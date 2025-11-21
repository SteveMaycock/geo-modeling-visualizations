# GEO7-Model-Vizualizations

This repository is used to process and visualize model data for the Global Environmental Outlook 7 report by UNEP. The repository is completely python based. 
The repository is divided into three main folders: data, plots, and src.

To install necessary packages use command ```pip install -r requirements.txt```.

### Data
In ```data/SOD``` are the most recent data files saved. 
- In the first level administration files are saved.
- In ```data/SOD/RCMIP``` validation files are saved.
- In ```data/SOD/model_results``` the model data is saved. Where it is split into:
    - ```data/SOD/model_results/raw``` for non-processed model results
    - ```data/SOD/model_results/chapter_19``` for non-processed model results for income groups used by chapter 19
    - ```data/SOD/model_results/processed``` for intermediate processed model results
    - ```data/SOD/model_results/to_share``` for final model results that are cleaned and harmonized and ready to use.

### Plots
In ```plots/SOD``` are the relevant plots saved. 
- chpt_11 and chpt_12 are divided by a diagnostic and report folder. Report folder contains figures that are used in the report. Diagnostic folder contais figures that provide background information. 
- chpt_19 contains folders for income groups, and for income and density groups. Income groups are primary used in the report. Income and density groups provide background information. 
- chpt_20 is divided by the un regions. 
- systems contain all stacked bars requested by the systems chapters.

### SRC
In ```src/SOD/models``` the data processing scripts of the models can be found.
- First run all the notebooks, order doesn't matter. In the second cell of the notebooks all input paths are found, change the path if you have new data.
- Then run data_to_share.py
- Finally, run data_slicing.py

The chapter specific folders all contain code for vizualizations. There is a lot of repeated code in the notebooks here, because of many ad-hoc requests. There is a plotting file in the ```src/SOD/utils``` folder, but it there were too many exceptions needed for the chapters to really use it efficiently. 