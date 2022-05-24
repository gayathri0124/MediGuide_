import numpy as np
import io

def search_state(df):
    state = df['State'].unique().tolist()

    return state

def fetch_state_hospital(df, state):
    global temp_df
    temp_df = df.drop_duplicates(subset=[ 'State'])

    x = df.loc[df['State']==state]
    #x['Pincode'] = x['Pincode'].astype('int')
    return x

def search_hospital(df):
    hosp = df['Hospital'].unique().tolist()

    return hosp

def fetch_hospital(df, hospital):
    x = df.loc[df['Hospital'] == hospital]

    return x

def search_city(df):
    city = df['City'].unique().tolist()

    return city

def fetch_city_hospital(df, city):
    global temp_df
    temp_df = df.drop_duplicates(subset=['City'])
    x = df.loc[df['City'] == city]
    x['Pincode'] = x['Pincode'].astype('int')
    return x

def search_pincode(df):
    pincode = df['Pincode'].unique().tolist()

    return pincode

def fetch_pin_hospital(df, pincode):
    global temp_df
    x = df[df['Pincode'] == (pincode)]
    x['Pincode'] = x['Pincode'].astype('str')
    return x

def search_allgs(gdf):
    allGS = gdf['State'].unique().tolist()

    return allGS

def fetch_all_govschemes(gdf):
    global temp_df
    return gdf

def search_stategs(gdf):
    allGS = gdf['State'].unique().tolist()

    return allGS

def fetch_state_gs(gdf, sgs):
    global temp_df
    x = gdf[gdf['State'] == sgs]
    return x
