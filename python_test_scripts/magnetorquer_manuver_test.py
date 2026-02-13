"""
Simple Magnetorquer Model & Manuver Test
----------------------------------
Tests the magnetorquer model by applying different currents to a magnetorquer over a few time intervals, 
and displays these maneuvers with VizKitPlanetRelative.

Author: Elias Dahl
"""
import sys
import site
import time
from pathlib import Path

##################################################################################
# Build path configuration. This tells the script where our custom models are.
# This must be included at the start of any script that uses custom models.

#This finds the folder where the script is
script_directory = Path(__file__).parent

# This looks up one folder into the main project folder, then looks down into the build folder, where the custom models are.
build_path_object = (script_directory / ".." / "build").resolve()

# This turns the Path object into a string for the lines below.
build_path = str(build_path_object)

# Force it to the FRONT of the search path
if build_path not in sys.path:
    sys.path.insert(0, build_path)

# Force Python to re-scan for namespace packages (Crucial for ModelSpace)
site.addsitedir(build_path)
##################################################################################

# Modelspace Imports
from modelspace.Spacecraft import Spacecraft
from modelspace.WorldMagneticFieldModel import WorldMagneticFieldModel
from modelspace.FrameStateSensorModel import FrameStateSensorModel
from modelspace.ModelSpacePy import SimulationExecutive, DEGREES_TO_RADIANS, connectSignals, CartesianVector3, Node, Time, DERIVATIVE
from modelspace.SpicePlanet import SpicePlanet
from modelspaceutils.vizkit.VizKitPlanetRelative import VizKitPlanetRelative

from modelspace.Magnetorquer import Magnetorquer

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


# Determine where the spacecraft is so we know the field at that pos.
pos_sensor = FrameStateSensorModel(exc, DERIVATIVE, "pos_sensor")

pos_sensor.params.target_frame_ptr(sc.body())                 
pos_sensor.params.reference_frame_ptr(earth.outputs.rotating_frame())

# Set up magnetic field
mag_field = WorldMagneticFieldModel(exc, DERIVATIVE, "mag_field")

connectSignals(pos_sensor.outputs.pos_tgt_ref__out, mag_field.inputs.pos_body_planet__pcr)

# Creates the torquer model
magnetorquer = Magnetorquer(exc, DERIVATIVE, "magnetorquer")

# Set m_prime based on orientation of the rod, on x-axis here.
# Value from aidan sim
magnetorquer.params.m_prime(CartesianVector3([0.36674, 0.0, 0.0]))

# Connect field to torquer. 
connectSignals(mag_field.outputs.mag_field__NED, magnetorquer.inputs.B)

# Creates a node that the torquer model will output torque to, and connect it to the spacecraft.
magnetorquer_node = Node("magnetorquer_node", sc.body())

# Connect the torquer model output to the torque node input
connectSignals(magnetorquer.outputs.torque, magnetorquer_node.moment)

# Set up planet vizkit, which displays our spacecraft and earth.
vk = VizKitPlanetRelative(exc)
# Adds earth to the vizkit
vk.planet(earth.outputs.inertial_frame())

# Adds the spacecraft to the vizkit. Both are necessary.
vk.target(sc.body())
vk.addSpacecraft(sc.body())

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
        # Applies no torque/ current.
        magnetorquer.inputs.I(0)
    elif current_time < 10.0:
        # Spin
        magnetorquer.inputs.I(0.001)
    elif current_time < 20.0:
        # Spin the other way!
        magnetorquer.inputs.I(-0.001)
    else:
         # Stop current/torque and drift
        magnetorquer.inputs.I(0)

    exc.step()

    # This slows down the loop to run in ~real time by stalling for a time step. 
    # Good for this short sim, but you'd want to speed this up for longer sims.
    time.sleep(1/float(SIMULATION_RATE_HZ))

    if current_time > 30.0:
        break
print("Sim end!")