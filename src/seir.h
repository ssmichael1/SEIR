#include <stdint.h>

#include <vector>

using ResultsType = std::vector<std::vector<double>>;

std::pair<double, double> R0TableType;

struct SEIR {
  public:
    SEIR();
    virtual ~SEIR(){};

    inline double R0(void) const { return R0_; }

    ResultsType compute(void);

    double R0_;           // Reproduction number
    double Tinc_;         // Incubation period
    double Tinf_;         // Infectious time constant
    double Tfat_;         // Fatal time constant
    double Tmrec_;        // Mild recovery time constant
    double Threc_;        // Hospital recovery time constant
    double pMild_;        // Probability of mild or no symptoms (no hospital)
    double pFat_;         // Probability of fatal if exposed
    double duration_;     // Simulation duration
    uint32_t population_; // Simulation capacity
    double dt_;           // time period between simulation outputs

    double Tintervention_;     // Time at start of intervention
    double Tintervention_end_; // Time at end of intervention
    double R0_reduction_;      // relative reduction of R0, in range [0, 1]

    double Hc_; // Hospital capacity, as fraction of total population, in range
                // [0, 1]
    double pfat_increase_nohospital_; // Incrase in fatal probability if no
                                      // hospital access
};
