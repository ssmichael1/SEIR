import numpy as np
from scipy.integrate import solve_ivp


class SEIR:
    """
    Susceptible
    Exposed
    Infectious
    Recovered/Removed

    Model of disease spread
    Inspired by:
    http://gabgoh.github.io/COVID/
    and described with great clarity in the paper he references:
    https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)30260-9/fulltext

    Modifications to "gabgoh" model:
    Includes a hospital capacity model
    Assumes probability of fatal outcome given exposure is function of hospitalized
    population being below or above capacity:

    Planned modifications:
    Separate out states of ODE into different age groups,
    Make R0 a matrix such that outcomes can be estimated if
    only certain population groups are isolated

    Author: Steven Michael (smichael@ll.mit.edu)
      Date: 3/28/2020
    """

    def __init__(self, **kwargs):

        """
        Note: all time units are days
        """

        # Reproduction number
        self.R0 = kwargs.get("R0", 3.2)
        # Time at public intervention
        self.T_intervention = kwargs.get("T_intervention", -1)
        # R0 reduction percentage at time of intervention
        self.R0_reduction = kwargs.get("R0_reduction", 0.75)
        # 1/e incubation perioud
        self.T_inc = kwargs.get("T_inc", 2)
        # 1/e infectuous period
        self.T_inf = kwargs.get("T_inf", 5)
        # 1/e mild recovery time
        self.T_mild_recovery = kwargs.get("T_mildrecover", 12)
        # 1/e time to hospital if severe symptoms
        self.T_hos = kwargs.get("T_tohospital", 5)
        # 1/e time to recovery in hospital if severe
        self.T_severe_recovery = kwargs.get("T_severerecover", 30)
        # 1/e time to death in hospital if fatal
        self.T_fatal = kwargs.get("T_fatal", 30)
        # Probability of fatal if exposed and with hospital access
        self.p_fatal = kwargs.get("p_fatal", 0.01)
        # Probabiliyt of fatal if exposed and no hospital access
        self.p_fatal_nohos = kwargs.get("p_fatal_nohospital", 0.05)
        # Initial population size
        self.population = kwargs.get("population", 1000000)
        # Duration of simulatin in days
        self.sim_duration = kwargs.get("duration", 300)
        # hospital capacity, as percent of population
        self.Hc = kwargs.get("hospital_capacity", 1)
        # probability of severe symptoms, given exposure
        self.p_severe = 1.0 - kwargs.get("p_mild", 0.8)
        self.p_severe = kwargs.get("p_severe", self.p_severe)

        # rate at which to compute output
        self.dt = 1

    def __str__(self):
        s = "" + (
            "S(usceptible), E(exposed), I(nfected), R(emoved) Model\n"
            + "                                       R0: %.2f\n" % self.R0
        )
        if self.T_intervention > 0:
            s = s + (
                ""
                + "                        Intervention Time: %d Days\n"
                % self.T_intervention
                + "             R0 Reduction at Intervention: %.2f%%\n"
                % (self.R0_reduction * 100)
            )
        s = s + (
            ""
            + "                               Population: %d\n"
            % self.population
            + "                        Incubation Period: %.2f Days\n"
            % self.T_inc
            + "                        Infectious Period: %.2f Days\n"
            % self.T_inf
            + "                            Mild recovery: %.2f Days\n"
            % self.T_mild_recovery
            + "                          Severe recovery: %.2f Days\n"
            % self.T_severe_recovery
            + "                    Probability of severe: %.2f\n"
            % self.p_severe
            + "                     Probability of fatal: %.2f\n" % self.p_fatal
            + "    Probability of non-hospitalized fatal: %.2f\n"
            % self.p_fatal_nohos
            + "                        Hospital capacity: %.2f%% of population\n"
            % (self.Hc * 100)
            + "                      Simulation Duration: %d Days\n"
            % self.sim_duration
        )
        return s

    @property
    def nsteps(self):
        return int(self.sim_duration / self.dt)

    @property
    def p_mild(self):
        return 1.0 - self.p_severe

    @p_mild.setter
    def p_mild(self, p):
        self.p_severe = 1.0 - p

    def dict_state(self, state, t):
        """
        Return ODE output as dictionary
        """
        return {
            "time": t.tolist(),
            "susceptible": state[0, :].tolist(),
            "exposed": state[1, :].tolist(),
            "infectious": state[2, :].tolist(),
            "mild": state[3, :].tolist(),
            "severe": state[4, :].tolist(),
            "hospitalized": state[5, :].tolist(),
            "fatal": state[6, :].tolist(),
            "recovered": state[7, :].tolist(),
        }

    def compute(self):
        """
        State is [suceptible, exposed, infectious,
                  mild, severe, hospital, fatal, recovered/removed]
        """

        # State for ODE has 8 elements
        state0 = np.zeros((8,), np.float64)
        # Susceptible population, normalized to 1
        state0[0] = 1
        # Initial number of exposed people
        # (here assumed to be 1)
        state0[1] = 1 / self.population

        # Integrate ordinary differential equation
        # This works pretty well for integrating through
        # discontinuity at intervention, but if I were
        # worried about speed and perfect accuracy,
        # I would split this into two itegrations
        sol = solve_ivp(
            self.statedot,
            [0, self.sim_duration],
            state0,
            t_eval=np.arange(0, self.sim_duration, self.dt),
            method="RK45"
            # method="DOP853",  # Dormund-prince
        )
        # Return output as dictionary
        return self.dict_state(sol.y * self.population, sol.t)

    def statedot(self, t, state):
        """
        The time derivative function for the ODE
        """

        # reproduction number,
        # number of infected people an exposed person will create
        # if entire population is susceptible
        R0 = self.R0

        # reduce the R0 if this is post-intervention
        if (self.T_intervention > 0) and (t > self.T_intervention):
            R0 = R0 * (1.0 - self.R0_reduction)

        S = state[0]  # Susceptible
        E = state[1]  # Exposed
        Infected = state[2]  # Infected
        M = state[3]  # Mild
        Se = state[4]  # Severe
        H = state[5]  # Hospitalized
        # F = state[6]  # Fatal (deaths)
        # R = state[7]  # Removed / Recovered

        # Probability of fatal given severe in hospital
        p_fs_hos = self.p_fatal / self.p_severe
        # probabiliyt of fatal given severe, not in hospital
        p_fs_nohos = self.p_fatal_nohos / self.p_severe
        # probabiilty of fatal, given severe
        if H == 0.0:
            p_fs = p_fs_hos
        else:
            p_fs = (
                max(0, 1 - (self.Hc / H)) * p_fs_nohos
                + min(1, self.Hc / H) * p_fs_hos
            )

        # Susceptible population
        # out: Susceptible people becoming exposed
        dS = -R0 / self.T_inf * Infected * S

        # Exposed population
        # in: Susceptible people becoming exposed
        # out: exposed people becoming infectious
        dE = -dS - E / self.T_inc

        # Infectious population
        # in: exposed people becoming infectious
        # out: Infected people no longer being infectious, but showing symptoms
        dI = E / self.T_inc - Infected / self.T_inf

        # Mild symptoms population
        # in: infected people expressing mild symptoms, no longer infecting
        # out: mild symptom people recovering
        dM = self.p_mild * Infected / self.T_inf - M / self.T_mild_recovery

        # Severe symptom population
        # in: infected people expressing severe symptoms, no longer infecting
        # out: severe symptom people going to hospital
        dSe = self.p_severe * Infected / self.T_inf - Se / self.T_hos

        # Hospitalization population
        # in: severe system people going to hospital
        # out 1: hospitalized patients dying
        # out 2: hospitalized patients recovering
        dH = (
            Se / self.T_hos
            - p_fs * H / self.T_fatal
            - (1 - p_fs) * H / self.T_severe_recovery
        )

        # Fatal cases
        # in: hospitalized with severe systems dying
        dF = p_fs * H / self.T_fatal

        # Recovered, no-longer susceptible (removed)
        # in 1: mildly symptomatic people recovering
        # in 2: hospitalized patients recovering
        dR = M / self.T_mild_recovery + (1 - p_fs) * H / self.T_severe_recovery

        statedot = np.array([dS, dE, dI, dM, dSe, dH, dF, dR])
        return statedot


if __name__ == "__main__":
    seir = SEIR()
    print(seir)
    d = seir.compute()
    print(d["susceptible"][-1])
    print(d["fatal"][-1])
    print(d["recovered"][-1])
