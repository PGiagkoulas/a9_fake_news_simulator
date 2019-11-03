# Fake news simulation
Simulation project for the course Design of Multi-agent Systems (2019-2020) in Rijksuniversiteit Groningen.

## Requirements
We suggest the use of Anaconda or Miniconda to create the environment:

[Miniconda](https://conda.io/en/latest/miniconda.html)

[Anaconda](https://www.anaconda.com/distribution/)

You can follow [this](https://problemsolvingwithpython.com/01-Orientation/01.05-Installing-Anaconda-on-Linux/) tutorial to install anaconda on linux.

## Environment
To install the environment, while in the source directory of this package, run:
```bat
conda env create -f environment.yml
```
If you are using linux and you get an error regarding access rights go to ~/anaconda3 and run

```bat
sudo chown --recursive yourUserName .

```
and then create the environment again.

Then run
```bat
conda activate fake_news_env

```
## Running the code
To run a simulation go to the a9_fake_news_simulator directory and run:
```bat
python main.py
```
After that follow the instructions. There is a choice between setting the parameters for the simulation by hand, through the command line commands or load an existing experiment set-up from a file.

## Creating an experiment set-up file
The file should be in a simple .txt format and the layout of the file should be the following:
* n_agents [value]
* n_liars [value]
* n_experts [value]
* n_connections [value]
* cluster_distance [value]
* n_news [value]
* n_steps [value]
* connectivity_type [value]
* communication_protocol [value]
* conversation_protocol [value]
* runs [value]

