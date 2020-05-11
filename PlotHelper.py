import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
#import plotly.graph_objects as goafrsdsa
from sklearn.impute import SimpleImputer


def getDataFrame(dataset = 'covid_19_data'):
    df = pd.read_csv('./novel-corona-virus-2019-dataset/covid_19_data.csv',parse_dates=['Last Update'])
    df.rename(columns={'ObservationDate':'Date', 'Country/Region':'Country'}, inplace=True)

    df_confirmed = pd.read_csv("./novel-corona-virus-2019-dataset/time_series_covid_19_confirmed.csv")
    df_recovered = pd.read_csv("./novel-corona-virus-2019-dataset/time_series_covid_19_recovered.csv")
    df_deaths = pd.read_csv("./novel-corona-virus-2019-dataset/time_series_covid_19_deaths.csv")

    df_confirmed.rename(columns={'Country/Region':'Country'}, inplace=True)
    df_recovered.rename(columns={'Country/Region':'Country'}, inplace=True)
    df_deaths.rename(columns={'Country/Region':'Country'}, inplace=True)
    return df

def getSummaryDataset():
    df = pd.read_csv('../novel-corona-virus-2019-dataset/covid_19_data.csv',parse_dates=['Last Update'])
    df.rename(columns={'ObservationDate':'Date', 'Country/Region':'Country' ,'Province/State':'Province'}, inplace=True)
    
    # data cleaning process . We have to impute the missing values 
    imputer = SimpleImputer(strategy='constant')
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    #converting to datetime format
    #df['Date']=pd.to_datetime(df['Date'],format="%m/%d/%Y")
    #df['Last Update'] = pd.to_datetime(df['Last Update'])
    
    #convertint to number for a proper calculation
    df['Confirmed'] = pd.to_numeric(df['Confirmed'], errors='coerce')
    df['Recovered'] = pd.to_numeric(df['Recovered'], errors='coerce')
    df['Deaths'] = pd.to_numeric(df['Deaths'], errors='coerce')
    df["TotalCases"]=df["Confirmed"]+df["Recovered"]+df['Deaths']
    return df

def get_Dates(df):
    result  = df[df['Date'].notnull()]['Date'].unique()
    return list(result)

def get_Countries(df):
    result  = df[df['Country'].notnull()]['Country'].unique()
    return list(result)


def get_Province(df):
    result  = df[df['Province'].notnull()]['Province'].unique()
    return list(result)


def filterDataFrame(df, **kw):
    for i,j in kw.items():
        if j == 'Any':
            continue

        df = df[df[i] == j]
    return df

def get_dates_in_between(df, start, end):
    
    #if start=='':
    #    start= '01/22/2020'
    #if end=='':
    #    end= '04/13/2020'
    df[start]
    years = df[(df["Confirmed"]== end - start)]
    
        #else

    return years