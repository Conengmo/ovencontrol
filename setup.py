import setuptools

# Install localy without copying files by running this pip command:
# pip install -e {path to the folder with this file}
# or on linux:
# pip install --user -e {path to the folder with this file}


setuptools.setup(
    name="ovencontrol",
    version="0.1",
    packages=setuptools.find_packages(),
)
