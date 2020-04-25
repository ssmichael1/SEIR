#include <seir.h>

#include <boost/numeric/odeint.hpp>

#include <iostream>
#include <functional>
#include <limits>

#include <math.h>
#if !defined(max)
#define max(a, b) (a > b ? a : b)
#endif

#if !defined(min)
#define min(a, b) (a < b ? a : b)
#endif

#define NSTATES 8
typedef std::array<double, NSTATES> StateType;

// odeing namespace access
namespace odeint = boost::numeric::odeint;

SEIR::SEIR()
    : R0_(3.2), Tinc_(2.5), Tinf_(5.0), Tfat_(30), Tmrec_(12), Threc_(30),
      pMild_(0.8), pFat_(0.01), duration_(300), population_(1000000), dt_(1),
      Tintervention_(0), Tintervention_end_(0), R0_reduction_(0), Hc_(1),
      pfat_increase_nohospital_(1.0)
{
}

ResultsType SEIR::compute(void)
{
    StateType state0;
    memset(state0.data(), 0, sizeof(double) * NSTATES);
    state0[0] = 1.0;
    state0[1] = 1.0 / (double)population_;

    typedef odeint::runge_kutta_cash_karp54<StateType, double, StateType,
                                            double>
        error_stepper_type;
    typedef odeint::controlled_runge_kutta<error_stepper_type>
        controlled_stepper_type;
    // typedef odeint::dense_output_runge_kutta<controlled_stepper_type>
    //   dense_stepper_type;

    // Create an output
    double nsteps = (double)duration_ / (double)dt_;
    if (::fmod(nsteps, 1.0) < std::numeric_limits<double>::epsilon())
        nsteps = nsteps + 1;
    else
        nsteps = ::ceil(nsteps);

    ResultsType results;
    results.resize((int)nsteps);
    uint32_t counter = 0;

    error_stepper_type stepper;
    odeint::integrate_const(
        stepper,
        [this](const StateType &state, StateType &statedot, double t) {
            // statedot.resize(NSTATES);

            double S = state[0];   // susceptible
            double E = state[1];   // exposed
            double Inf = state[2]; // Infectious
            double M = state[3];   // Mild case
            double Hrec = state[4];
            double Hfat = state[5];

            // Probability of fatal given hospitalized
            // and sufficient hospital capacity
            double pfs_hos = pFat_ / (1.0 - pMild_);

            // Probability of fatal given hospitalized,
            // and no hospital capacity
            double pfs_nohos = pfs_hos * (1.0 + pfat_increase_nohospital_);

            // weighted probability of fatal
            // given hospital capacity
            double H = Hrec + Hfat;
            double pfs = pfs_hos;
            if ((H > Hc_) && (H > 0)) {
                pfs = (Hc_ / H) * pfs_hos + (H - Hc_) / H * pfs_nohos;
            }

            // Instantaneous R0
            // (are we in the middle of an intervention period)
            double R0 = R0_;
            if ((Tintervention_ > 0) && (t > Tintervention_)
                && (t < Tintervention_end_)) {
                R0 = R0 * (1.0 - R0_reduction_);
            }

            // Update time derivates:

            // Susceptible population:
            // out: susceptible to exposed
            auto dS = -R0 / Tinf_ * Inf * S;
            // Exposed population:
            // in: susceptible to exposed
            // out: exposed to infectious
            auto dE = -dS - E / Tinc_;
            // Infectious population:
            // in: exposed to infectious
            // out: infectious to mild or hospital
            auto dI = E / Tinc_ - Inf / Tinf_;
            // Mild case population:
            // in: infectious to mild
            // out: mild to recovered (removed)
            auto dM = pMild_ * Inf / Tinf_ - M / Tmrec_;
            // Hospitalized population that will recover
            // in: infectious to hospitalized
            // out: hospitalized to recovered
            auto dHrec =
                (1.0 - pMild_) * (1.0 - pfs) * Inf / Tinf_ - Hrec / Threc_;
            // Hospitalized population that will not recover
            // in: infectious to hospitalized
            // out: hospitalized to fatal
            auto dHfat = (1.0 - pMild_) * pfs * Inf / Tinf_ - Hfat / Tfat_;
            // Fatal population:
            // in: hospitalized to fatal
            auto dF = Hfat / Tfat_;
            // Removed population:
            // in: mild to recovered
            // in: hospitalized to recovered
            auto dR = M / Tmrec_ + Hrec / Threc_;

            statedot[0] = dS;
            statedot[1] = dE;
            statedot[2] = dI;
            statedot[3] = dM;
            statedot[4] = dHrec;
            statedot[5] = dHfat;
            statedot[6] = dF;
            statedot[7] = dR;
        },
        state0, 0.0, (double)duration_, dt_,
        [this, &counter, &results](const StateType &s, double t) {
            results[counter] = std::vector<double>(s.begin(), s.end());
            counter++;
        });

    // Multiply results by population
    double population = this->population_;
    for (auto &res : results) {
        std::transform(res.begin(), res.end(), res.begin(),
                       [population](double &c) { return population * c; });
    }
    return results;
}

#if 1
int main(int argc, char *argv[])
{
    SEIR seir;
    seir.Hc_ = .001;
    auto results = seir.compute();
    auto lr = results[results.size() - 1];
    for (int i = 0; i < NSTATES; i++) {
        std::cout << lr[i] << std::endl;
    }
    return 0;
}
#endif
