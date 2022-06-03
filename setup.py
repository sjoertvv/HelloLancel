import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hellolancel",
    version="0.1.0",
    author="Sjoert van Velzen, Robert Stein",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/winter-telescope/wintertoo",
    keywords="astronomy IceCube neutrino",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires='>=3.7',
    install_requires=[
        "aplpy",
        "astropy",
        "k3match @ https://github.com/pschella/k3match/archive/51a49a83d36bd5289bcd1c03296cf20531b4c924.zip",
        "matplotlib",
        "numpy",
        "pyregion",
        "requests",
        "scipy",
        "sjoert @ https://github.com/sjoertvv/sjoert/archive/fac5635b8d1f2a8dbcc6cdb5eec800e578d54054.zip",
    ],
    package_data={
        'hellolancel': [
            'data/2MASS/*.fit',
            "data/IC/*",
            "data/ZTF_NEOWISE/*.dat"
        ],
    }
)
