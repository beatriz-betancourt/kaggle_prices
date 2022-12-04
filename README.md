# kaggle_prices

Simple ML model that predicts price for Kaggle Competition [**Predict Future Sales**](https://www.kaggle.com/competitions/competitive-data-science-predict-future-sales) 

Main function main.py is under the **applications** directory

---
## Repository Structure:
**utils folder** 
-  *Data* class has I/O function for csv files
-  *Logger* class handles logging information

**model folder** 
-  *Feature* class   related to create features from data
-  *LinearModels* class that contains functions for saving details of the Linear models implemented
- *GeneralModel* class is base estimator class that handles different Regression Models

**prep folder** 
- *Format* class  has functions that gives format to dataframes
- *PrepTime*      has functions to clean data based on time dependence 
- *Prep*          has functions to format and clean data for training 

**visual folder**
- *Plots* class has predefined functions to visualize dataframes in 3d

**Defaults.py** has all static settings of the repository like information of location of data, run_indicator, etc.
