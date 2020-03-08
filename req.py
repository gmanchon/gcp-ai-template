import os
import sys

# interprets python code passed as argument to define REQUIRED_PACKAGES
# which is supposed (haha) to contain a list of packages and versions
exec(sys.argv[1])

# installs all packages
for package_requirement in REQUIRED_PACKAGES:
    os.system(f'pip install {package_requirement}')
