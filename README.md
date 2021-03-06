# SLACTest

Simultaneously localization and configuration (SLAC) for sensor networks. Uses GP-LVM 
(Guassian Process Latent Variable Models) to find latent position of nodes.

## Requirements

Apart from Python 2 (tested on 2.7), the following must be installed on your system:

* GPy
* Matplotlib
* Numpy
* Scipy

All of these can be installed using _pip_:

	pip install <module>

## Running the examples

To run the GP-LVM prediction first generate a data file:

	python src/generateData.py
	
This generates a numpy data file containing a network simulation. Now you can run the prediction algorithm:

	python src/predict.py
	
## Example movies

See _/examples_ for a collection of sample movies.

## Configuration

The GP-LVM model can be tweaked. To enable custom configuration rename _.gpy_user.cfg.example_ to _.gpy_user.cfg_
and place it in your HOME or USERPROFILE directory.

It is advised to disable Weave.