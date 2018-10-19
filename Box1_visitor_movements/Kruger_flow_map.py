# -*- coding: utf-8 -*-
"""
Script for identifying the most probable home country for Instagram users that have visited Kruger national park, SA.
The script calculates following things:
    - Specify country etc. for each post 
    - Calculate the country with 1) most posts and 2) second most posts
    - Calculate the distance of users movements (Great Circle distance in km)
    - Calculate the time spent in Kruger national park 
    - Calculate and create a Shapefile where there is the amount of Instagram users in each country

Code associated to following manuscript:
    
    DGL 2019. "Social media data for conservation science: a methodological overview."
    
Author: 
    Henrikki Tenkanen, Digital Geography Lab, Department of Geosciences and Geography, University of Helsinki.

Requirements:
    geopandas
    pandas
    shapely
    matplotlib
    datetime
    fiona
    numpy
    

Created on:
    Mon May 22 17:49:21 2017

License:
    Creative Commons BY 4.0. See details from https://creativecommons.org/licenses/by/4.0/
"""


import geopandas as gpd
import pandas as pd
from datetime import datetime
from shapely.geometry import Point, LineString, MultiLineString
from fiona.crs import from_epsg
import numpy as np
import matplotlib.pyplot as plt
from spatial_tools import *
from Draw_Great_Circle_Paths import greatCircleRoute

def pointInPolygon(point_df, poly_df, poly_rtree, sourceColumn_in_poly, targetColumn_in_point, fast_search=True):
    """Iterates over points"""
    data = point_df
    data[targetColumn_in_point] = None
    data[targetColumn_in_point] = point_df.apply(querySpatialIndex, axis=1, poly_df=poly_df, poly_rtree=poly_rtree, source_column=sourceColumn_in_poly)
    return data

def querySpatialIndex(point, poly_df, poly_rtree, source_column):
    """Find poly containing the point"""
    point_coords = point['geometry'].coords[:][0]
    for idx_poly in poly_rtree.intersection( point_coords ):
        if poly_df['geometry'][idx_poly:idx_poly+1].values[0].contains(point['geometry']):
            return poly_df[source_column][idx_poly:idx_poly+1].values[0]
    return None

def buildRtree(polygon_df):
    idx = index.Index()
    for poly in polygon_df.iterrows():
        idx.insert(poly[0], poly[1]['geometry'].bounds)
    return idx

def pointCoords(point_list):
    return [(point.x, point.y) for point in point_list]

def createPolyline(point_list):
    return LineString(pointCoords(point_list))

def calculateTimeDelta(df):
    df['delta'] = (df['time']-df['time'].shift()).fillna(0)
    return df

def filterVisits(df, t_threshold):
    # Create visit index
    df['visitidx'] = 0
    # Column for time windows
    df['timewindow'] = None
    # Column for visit time in hours
    df['visit_h'] = None
    # Reset index
    df = df.reset_index()
    if df['delta'].max() > t_threshold:
        # Iterate over values and split data into separate DataFrames
        visit_idx = 1
        start_idx = 0
        # Start time
        start_time = df.loc[0, 'time']
        # Get the start date of visit
        start_date = start_time.strftime("%Y/%m/%d")
        # Iterate over rows 
        for idx, row in df.iterrows():
            if row['delta'] > t_threshold:
                # Select visit values
                df.ix[start_idx:, 'visitidx']=visit_idx
                # Set start_idx
                start_idx = idx
                # Set visit idx
                visit_idx+=1
                # End time
                end_time = df.loc[idx, 'time']
                # Get end date
                end_date = end_time.strftime("%Y/%m/%d")
                # Make time window
                timewindow = "%s - %s" % (start_date, end_date)
                # Calculate visit length in hours
                df['visit_h'] = round((end_time - start_time).seconds/60/60)
                # Set timewindow
                df.ix[start_idx:,'timewindow']=timewindow
                # Reset start_time / date
                start_date = end_date
                start_time = end_time
                
        # Build DateTime index back again
        df = df.set_index(pd.DatetimeIndex(df['time']))
        return df
    else:
        # Get the start time of visit
        start_time = df.loc[0, 'time']
        # Get the start date of visit
        start_date = start_time.strftime("%Y/%m/%d")
        # Get end time
        end_time = df.iloc[-1]['time']
        # Get end date
        end_date = end_time.strftime("%Y/%m/%d")
        # Calculate visit length in hours
        df['visit_h'] = round((end_time - start_time).seconds/60/60)
        # Make time window
        timewindow = "%s - %s" % (start_date, end_date)
        df['timewindow'] = timewindow
        return df
    
# Filepaths
# =========

# Input data
fp = "/data/Instagram_Kruger_VisitorHistory_movements_CountryCodes.shp"
user_fp = "/data/Instagram_Kruger_2013-2015_October.shp"
c_fp = "/data/World_countries.shp"
outfp = "/data/Instagram_Global_Kruger_VisitorHistory_trips_to_Kruger_basedOn_probableHomeCountry_GreatCircle.shp"
knp_fp = "/data/Kruger_NP_boundaries_2014.shp"

# UserID dataset that were used to collect visitor mobilities
# ...........................................................
users = gpd.read_file(user_fp)
userids = users['userid'].unique()

# Country borders ==> Change to World_regions.shp
world = gpd.read_file(c_fp)
za = world.ix[world['FIPS_CNTRY']=='SF'].copy()

# Create Spatial Index for the world
rtree = buildRtree(world)

# Kruger borders
knp = gpd.read_file(knp_fp)

# Project to WGS84
knp['geometry'] = knp['geometry'].to_crs(epsg=4326)

# Create a ~22 km (0.2 decimal degrees) buffer around KNP so that posts taken right next to Kruger are not taken into account as previous location
knp['geometry'] = knp['geometry'].buffer(0.2)

# Create Spatial Index for the KNP
knp_rtree = buildRtree(knp)

# PARAMETERS
# ==========

# Time window
start_date, end_date = datetime(2010,1,1,0,0,0), datetime(2016,6,1,0,0,0)

# Year
year = "2010-2016" #start_date.year

# Parse some file path
some = gpd.read_file(fp)

# Determine country for each post (already done at this time)
#some = pointInPolygon(point_df=some, poly_df=world, poly_rtree=rtree, sourceColumn_in_poly='FIPS_CNTRY', targetColumn_in_point='FIPS_CNTRY')

# Create datetime index from timestamps
some = some.sort_values(by='time_local')
some = some.reset_index(drop=True)
some['time'] = pd.to_datetime(some['time_local'])
some = some.set_index(pd.DatetimeIndex(some['time']))

# Take a selection
some = some[start_date:end_date]

# Select only users that have for sure been in Kruger (the API returned also some random users from Finland when collecting the data)
selected = some.ix[some['userid'].isin(userids)]

# -----------------------------------
# Determine the last country 
# -----------------------------------

# Determine if the post is from Kruger (with 22km buffer) or not
selected = pointInPolygon(point_df=selected, poly_df=knp, poly_rtree=knp_rtree, sourceColumn_in_poly='NAME', targetColumn_in_point='FromKruger')

# Group by individual users
grouped = selected.groupby('userid')

# Create GeoDataFrame for the results
geo = gpd.GeoDataFrame(crs=from_epsg(4326))

# Counter for the users who posted their first Instagram post from Kruger
kruger_was_first = 0

# Flag for identifying country
identify_country = True

# FIPS code of the country where the national park is located
#country_fips = "SF"

# Minimum amount of posts to determine the home location
min_posts = 20 #30

# Create Polylines between the previous location to Kruger for users within South-Africa
for userid, data in grouped:
    # If there are more points than 1, create a movement pattern
    if len(data) > min_posts:
        # Get the Kruger point from user-data
        userdata = users.ix[users['userid']==userid]
        # The earliest time when arriving to Kruger
        userdata = userdata.sort_values(by='time_local')
        userdata = userdata.reset_index(drop=True)
        first_knp_time = userdata.loc[0,'time_local']
        first_knp_geom = userdata.loc[0,'geometry']

        # The country with most posts
        cntry_counts = data['FIPS_CNTRY'].value_counts()
        most_posts_1, photo_cnt_1 = cntry_counts.index[0], cntry_counts[0]

        # The country with second most posts
        try:
            most_posts_2, photo_cnt_2 = cntry_counts.index[1], cntry_counts[1]
        except:
            most_posts_2, photo_cnt_2 = "N/A", 0

        # Take posts that are from the most pro
        if identify_country:
            prev_posts = data.ix[(data['FIPS_CNTRY']==most_posts_1) & (data['FIPS_CNTRY']!='N/A')]

        if len(prev_posts) == 0:
            kruger_was_first += 1
        else:
            # Select the latest post that was not from Kruger
            prev_posts_outside_knp = prev_posts.ix[prev_posts['FromKruger'].isnull()]
            if len(prev_posts_outside_knp) == 0:
                kruger_was_first += 1
            else:
                previous_loc = prev_posts_outside_knp.tail(1)
                previous_geom = previous_loc['geometry'].values[0]
                previous_time = previous_loc['time_local'].values[0]

                # Calculate the time difference (in days) between posts
                tformat = "%Y-%m-%d %H:%M:%S"
                time_dif = datetime.strptime(first_knp_time, tformat) - datetime.strptime(previous_time, tformat)
                time_dif = time_dif.days

                # List shapely point objects
                points = [previous_geom, first_knp_geom]
                
                # Create a polyline out of points
                
                # Direct lines
                # ------------
                #line = createPolyline(points)
                
                # Great Circle Lines
                line = greatCircleRoute(ordered_point_list=points, del_s=100.0)
                
                # Calculate the distance between posts (in kilometers approximately)
                distance = line.length * 111.32

                # Get userid
                user = userid
                # Get number of posts
                count = len(data)
                # Append data to GeoDataFrame
                geo = geo.append([[user, count, line, distance, previous_time, first_knp_time, time_dif, most_posts_1, photo_cnt_1, most_posts_2, photo_cnt_2]])
    else:
        kruger_was_first += 1
            
# Set column names
geo.columns = ['userid', 'post_cnt', 'geometry', 'distance', 't_bef_KNP', 'arriv_to_KNP', 't_difference', 'Home1_cntr', 'Home1_cnt', 'Home2_cntr', 'Home2_cnt']
# Initialize GeoDataFrame again
geo = gpd.GeoDataFrame(geo, geometry='geometry', crs=from_epsg(4326))
# Reset index
geo = geo.reset_index(drop=True)

# Calculate the percentage of the 1st ranked country vs the second (to evaluate the accuracy)
geo['Home1_cnt%'] = geo['Home1_cnt'] / (geo['Home1_cnt'] + geo['Home2_cnt'])
geo['Home2_cnt%'] = geo['Home2_cnt'] / (geo['Home1_cnt'] + geo['Home2_cnt'])
geo.to_file(outfp)

