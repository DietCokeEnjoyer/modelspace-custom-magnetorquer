/*
Metadata for MS GUI:
imdata = {"displayname" : "Torquer Model",
          "exclude" : False,
          "category" : "Custom"
}
aliases = {"input_torque" : "Input Torque",
           "output_torque" : "Output Torque",
}
*/

#ifndef MODELS_TORQUER_H
#define MODELS_TORQUER_H

#include "simulation/Model.h"

#include "modelspace/core/Matrix.hpp" 
#include "modelspace/core/matrixmath.hpp"
#include "modelspace/core/vectormath.hpp"
#include "modelspace/core/mathmacros.h"
#include "modelspace/core/CartesianVector.hpp"
#include "modelspace/core/safemath.h"

namespace modelspace {

    /**
     * @brief   Simple implementation of a Torquer.
    */
    MODEL(Torquer)
    public:
        // Model params
        //         NAME                     TYPE                    DEFAULT VALUE
        START_PARAMS
            // DO we need any?
        END_PARAMS

        // Model inputs
        //         NAME                     TYPE                    DEFAULT VALUE
        START_INPUTS
            /** T */
            SIGNAL(input_torque,                       CartesianVector3,                 0)
        END_INPUTS

        // Model outputs
        //         NAME                     TYPE                    DEFAULT VALUE
        START_OUTPUTS
            /** The torque vector from the cross product of m x B */
            SIGNAL(output_torque,                       CartesianVector3,                 0.0)
        END_OUTPUTS

        int16 activate() override;
        int16 deactivate() override;

    protected:
        int16 start() override;
        int16 execute() override;
    };

}

#endif