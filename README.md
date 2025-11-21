# GEO7-Model-Vizualizations

This repository is used to process and visualize model data for the Global Environmental Outlook 7 report by UNEP. The repository is completely python based. 
The repository is divided into main folders: data and src.

To install necessary packages use command ```pip install -r requirements.txt```.

### Data
In ```data/TOD``` are the most recent data files saved. 
- In the first level administration files are saved.
- In ```data/TOD/RCMIP``` validation files are saved.
- In ```data/TOD/model_results``` the model data is saved. Where it is split into:
    - ```data/TOD/model_results/raw``` for non-processed model results
    - ```data/TOD/model_results/chapter_19``` for non-processed model results for income groups used by chapter 19
    - ```data/TOD/model_results/processed``` for intermediate processed model results
    - ```data/TOD/model_results/to_share``` for final model results that are cleaned and harmonized and ready to use.

### SRC
In ```src/TOD/models``` the data processing scripts of the models can be found. -> including harmonization between models (IMAGE and AIM) and regional aggregations used, unique for each model.
- First run all the notebooks, order doesn't matter. In the second cell of the notebooks all input paths are found, change the path if you have new data.
- Then run data_to_share.py
- Finally, run data_slicing.py


The chapter specific folders all contain code for vizualizations. There is a lot of repeated code in the notebooks here, because of many ad-hoc requests.
