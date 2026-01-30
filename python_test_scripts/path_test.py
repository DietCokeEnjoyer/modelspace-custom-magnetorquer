import sys
import os
import site

# 1. Define your build path explicitly
# (Double check this path matches exactly where your 'modelspace' folder is)
build_path_root = "/home/eliasrdahl/projects/modelspace-custom-magnetorquer/build"

# 2. Force it to the FRONT of the search path
if build_path_root not in sys.path:
    sys.path.insert(0, build_path_root)

# 3. THE TRICK: Force Python to re-scan for namespace packages
# This makes sure Python sees the 'pkgutil' instruction you added earlier
site.addsitedir(build_path_root)

# --- DEBUG PRINT ---
import modelspace
print(f"Modelspace path list: {modelspace.__path__}")
# You should see TWO paths printed above:
# 1. Your build folder
# 2. The /usr/lib/ system folder
# -------------------

from modelspace.Spacecraft import Spacecraft
# Now try importing your custom module
# import modelspace.YourCustomModule