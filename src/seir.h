#include <stdint.h>

#include <vector>
#include <utility>
#include <list>

using ResultsType = std::vector<std::vector<double>>;

using R0TableElement = std::pair<double, double>;
using R0TableType = std::list<R0TableElement>;

struct SEIR {
  public:
    SEIR();
    virtual ~SEIR(){};

    void SetR0(double R0, double time = -1);

    ResultsType compute(void);

    R0TableType R0Table_; // Table of R0 vs time
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
    double Hc_; // Hospital capacity, as fraction of total population, in range
                // [0, 1]
    double pfat_increase_nohospital_; // Incrase in fatal probability if no
                                      // hospital access
};
