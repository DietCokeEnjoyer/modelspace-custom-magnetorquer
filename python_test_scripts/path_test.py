"""
Build path setup test
----------------------------------
Our sims need to see both our custom model "modelspace" folder, as well as the main "modelspace" folder.
This script checks to see if both folders are visible to python.

Author: Elias Dahl
"""

import sys
import site
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

import modelspace
# This should print two file paths:
# 1. Your build folder
# 2. The /usr/lib/ system folder
print(f"Modelspace path list: {modelspace.__path__}")
