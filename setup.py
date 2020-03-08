from setuptools import find_packages
from setuptools import setup

from Model.conf import PACKAGE_NAME, REQUIRED_PACKAGES, PACKAGE_DESCRIPTION

setup(name=PACKAGE_NAME,
    version='1.0',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description=PACKAGE_DESCRIPTION)
