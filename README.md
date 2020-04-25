# Yet Another SEIR Model
Source code for website: https://yetanotherseirmodel.com

## Author: Steven Michael (ssmichael@gmail.com)

## Description

This web site represents a standard **SEIR** -- **S**usceptible **E**xposed **I**nfectious **R**emoved -- model for the spread of coummnicable disesase.  The model has some small additions to the basic SEIR model:

* Infectious state transitions to a mildly symptomatic state and a hospital state.  Hospital state can transition to fatal (detah) state
* Model allows for an intervention period in which the reproduction number, R0, is reduced. 
* Model allows for finite hospital capacity, with probability of death increasing when capacity is exceeded
  
The website provides complete model details.  The model is implemented in C++, and is compiled with emscripten to run natively in the web browser.

The website also plots data from the Johns Hopkins COVID-19 database - https://github.com/CSSEGISandData/COVID-19 - showing both deaths and confirmed cases as a function of country and US state.  The model parameters can then be tuned to match the statistics of the selected region.



