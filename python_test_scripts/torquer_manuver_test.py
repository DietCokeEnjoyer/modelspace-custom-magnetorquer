"""
Simple Torquer Model & Manuver Test
----------------------------------
Tests the simple torquer model and maneuver pattern by applying different torques
to a spacecraft over a few time intervals, and displays the maneuvers with VizKitPlanetRelative.

Author: Elias Dahl
"""
import sys
import site
import time

# Build path configuration, set this to the build directory of your repo.
build_path_root = "/home/eliasrdahl/projects/modelspace-custom-magnetorquer/build"

# Force it to the FRONT of the search path
if build_path_root not in sys.path:
    sys.path.insert(0, build_path_root)

# Force Python to re-scan for namespace packages (Crucial for ModelSpace)
site.addsitedir(build_path_root)

# Modelspace Imports
from modelspace.Spacecraft import Spacecraft
from modelspace.ModelSpacePy import SimulationExecutive, DEGREES_TO_RADIANS, connectSignals, CartesianVector3, Node, Time
from modelspace.SpicePlanet import SpicePlanet
from modelspaceutils.vizkit.VizKitPlanetRelative import VizKitPlanetRelative

from modelspace.Torquer import Torquer

# The simulation rate / time step size, e.g. 100Hz -> 0.1 sec time steps.
SIMULATION_RATE_HZ = 100
#### Script ####

exc = SimulationExecutive()     # Create our executive -- by convention named exc
exc.parseArgs(sys.argv)         # this interperets command-line inputs
exc.setRateHz(SIMULATION_RATE_HZ)                # Sets the simulation rate from our constant.

# Creates our planet model
earth = SpicePlanet(exc, "earth")

# Creates our spacecraft model and set it to orbit earth
sc = Spacecraft(exc, "sc")
sc.params.planet_ptr(earth)

# Creates the torquer model
torquer_model = Torquer(exc, "torquer_model")

# Creates a node that the torquer model will output torque to, and connect it to the spacecraft.
torquer_node = Node("torquer_node", sc.body())

# Connect the torquer model output to the torque node input
connectSignals(torquer_model.outputs.output_torque, torquer_node.moment)

# Set up planet vizkit, which displays our spacecraft and earth.
vk = VizKitPlanetRelative(exc)
# Adds earth to the vizkit
vk.planet(earth.outputs.inertial_frame())

# Adds the spacecraft to the vizkit. Both are necessary.
vk.target(sc.outputs.body())
vk.addSpacecraft(sc.outputs.body())

# Adds the vizkit to the simulation exc and sets its display rate.
exc.logManager().addLog(vk, SIMULATION_RATE_HZ)

### Simulation Initialization ###
exc.startup()

# Sets the inital values for the spacecraft's parameters.
sc.initializeFromOrbitalElements(7278137.0, 0.1, DEGREES_TO_RADIANS*40.0, DEGREES_TO_RADIANS*10.0, DEGREES_TO_RADIANS*10.0, DEGREES_TO_RADIANS*30.0)


## Simulation Loop ###
print("Sim start!")
while not exc.isTerminated():

    current_time = exc.time().base_time().asFloatingPoint()
    if current_time < 5.0:
        # Applies no torque.
        torquer_model.inputs.input_torque(CartesianVector3([0.0, 0.0, 0.0]))
    elif current_time < 10.0:
        # Applies 0.1 Nm torque on the X-axis.
        torquer_model.inputs.input_torque(CartesianVector3([0.1, 0.0, 0.0]))
    elif current_time < 20.0:
        # Applies -0.1 Nm torque on the X-axis
        torquer_model.inputs.input_torque(CartesianVector3([-0.1, 0.0, 0.0]))
    else:
         # Applies no torque.
        torquer_model.inputs.input_torque(CartesianVector3([0.0, 0.0, 0.0]))

    exc.step()

    # This slows down the loop to run in ~real time by stalling for a time step. 
    # Good for this short sim, but you'd want to speed this up for longer sims.
    time.sleep(1/float(SIMULATION_RATE_HZ))

    if current_time > 30.0:
        break
print("Sim end!")