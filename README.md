# Forward Protons short exercise for the 2020 CMSDAS

General information on CMSDAS 2020:
* [CMSDAS2020 main page](https://indico.cern.ch/e/cmsvdas2020)
* [All short exercises](https://twiki.cern.ch/twiki/bin/view/CMS/WorkBookExercisesCMSDataAnalysisSchool#CmsDas2020CERN)
* [Exercise Twiki](https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideCMSDataAnalysisSchoolCERN2020TaggedProtonsShortExercise)

**Video introduction**: [watch here!](https://videos.cern.ch/video/0000000)

### Recommended way to run the exercise (SWAN)
[![SWAN](https://swanserver.web.cern.ch/swanserver/images/badge_swan_white_150.png)](https://cern.ch/swanserver/cgi-bin/go/?projurl=https://github.com/cmsdas/pps-short-exercise.git)

To run the notebooks with regular CERN resources:
* Open a [SWAN session](swan.cern.ch) (the defaults are good, as of writing this pick software stack 97a and make sure to use Python3)
* In the SWAN session, click on the item on the right-hand side that says "Download Project from git"
* Copy-paste https://github.com/cmsdas/pps-short-exercise.git
* You're all set and can click on the three exercises, `Optical-Functions.ipynb`, `PixelEfficiencies.ipynb`, and `Dilepton-Protons.ipynb`

### Table of content

The exercise is organised in three Jupyter notebooks:

* [Optical functions](https://nbviewer.jupyter.org/github/cmsdas/pps-short-exercise/blob/master/Optical-Functions.ipynb)  
This notebook requires ROOT to be installed.
 
* [Tracker Efficiencies](https://nbviewer.jupyter.org/github/cmsdas/pps-short-exercise/blob/master/PixelEfficiencies.ipynb)  

* [PPS protons in dilepton events](https://nbviewer.jupyter.org/cmsdas/pps-short-exercise/blob/master/Dilepton-Protons.ipynb)  
The installation of the following packages is needed to run the notebook:  
`python3 -m pip install --user uproot4 awkward1 mplhep`  
Or in a virtual environment:  
`python3 -m venv myenv`  
`. myenv/bin/activate`  
`python3 -m pip install uproot4 awkward1 mplhep`

