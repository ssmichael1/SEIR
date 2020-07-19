
#include <emscripten/bind.h>

#include <vector>
#include <iostream>

#include <seir.h>

using namespace emscripten;

ResultsType testfunc(const val &v)
{
    static SEIR seir;
    seir.Tinc_ = v["Tinc"].as<double>();
    seir.Tinf_ = v["Tinf"].as<double>();
    seir.Tmrec_ = v["Tmrec"].as<double>();
    seir.Threc_ = v["Threc"].as<double>();
    seir.Tfat_ = v["Tfat"].as<double>();
    seir.pMild_ = v["pMild"].as<double>();
    seir.pFat_ = v["pFatal"].as<double>();
    seir.duration_ = v["duration"].as<double>();
    seir.population_ = v["population"].as<int>();
    seir.dt_ = v["dt"].as<double>();

    seir.R0Table_.clear();
    double R0 = v["R0"].as<double>();
    double intervention_r0 = R0 * (1.0 - v["R0_reduction"].as<double>());
    double intervention_time = v["Tintervention"].as<double>();
    double intervention_end =
        intervention_time + v["intervention_duration"].as<double>();
    seir.R0Table_.push_back(R0TableElement(R0, 0));
    seir.R0Table_.push_back(R0TableElement(intervention_r0, intervention_time));
    seir.R0Table_.push_back(R0TableElement(R0, intervention_end));

    seir.Hc_ = v["Hc"].as<double>();
    seir.pfat_increase_nohospital_ = v["pfat_increase_nohos"].as<double>();

    auto results = seir.compute();
    auto N = results.size();
    double dt = seir.dt_;
    for (auto i = 0; i < N; i++) {
        results[i].push_back((double)i * dt);
    }
    return results;
}

EMSCRIPTEN_BINDINGS(example)
{
    function("seir", &testfunc);
    register_vector<double>("dvec");
    register_vector<std::vector<double>>("ddvec");
}
