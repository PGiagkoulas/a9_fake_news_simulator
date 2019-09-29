# Fake news simulation
Simulation project for the course Design of Multi-agent Systems (2019-2020) in Rijksuniversiteit Groningen.

## Requirements
We suggest the use of Anaconda or Miniconda to create the environment:

[Miniconda](https://conda.io/en/latest/miniconda.html)

[Anaconda](https://www.anaconda.com/distribution/)

You can follow [this](https://problemsolvingwithpython.com/01-Orientation/01.05-Installing-Anaconda-on-Linux/) tutorial to install anaconda on linux.

## Environment
First deactivate the current environment, if there is any activated by running 
```bat
conda deactivate
```
To install the environment, while in the source directory of this package, run:
```bat
conda env create -f environment.yml
```
If you are using linux you get an error regarding access rights go to ~/anaconda3 and run

```bat
sudo chown --recursive yourUserName .

```
## Running the code
To run a simulation, run:
```bat
python main.py
```
