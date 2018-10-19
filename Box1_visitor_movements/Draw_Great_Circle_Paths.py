# -*- coding: utf-8 -*-
"""
Draw_Great_Circle_Paths.py

Created on Fri Oct  7 10:01:46 2016

Description:
------------
This simple script and the functions can be used to calculate create Great Circle Paths (curvy lines)
between two points (origin and destination) that should be Shapely.Point -objects in WGS84 projection (lat, lon -format). 

The function greatCirclePath returns a Shapely.LineString -object of the GreatCirclePath that was calculated between origin and destination
points. 

The function greatCircleRoute calculates Great Circle Routes between multiple input Points that will be combined into a single LineString.
The order of the points in a list determines how the lines are drawn (created in a consecutive manner).

Parameters:
-----------

greatCirclePath (orig_point, dest_point, del_s):
  orig_point: Origin point as Shapely.Point -object in WGS84 projection (lat, lon format)
  dest_point: Destination point as Shapely.Point -object in WGS84 projection (lat, lon format)
  del_s: Points on great circle computed every del_s kilometers (default 100).

greatCircleRoute (ordered_point_list, del_s=100.0):
  ordered_point_list: a list of Shapely.Point -objects in WGS84 projection. The order of the points determines how the route is formed.
  del_s: Points on great circle computed every del_s kilometers (default 100).


Requirements:
-------------    
    
Requires following Python modules to be installed:
    
    matplotlib
    matplotlib.Basemap
    shapely
    numpy

Usage:
------    

An example use-case where we calculate the Great Circle Path between Helsinki and New York:
    
    # nylat, nylon are lat/lon of New York
    nylat = 40.78; nylon = -73.98
    
    # hellat, hellon are lat/lon of Helsinki.
    hellat = 60.17083; hellon = 24.93750
    
    # Create a Shapely Points out of the coordinates (most commonly all data are stored as Shapely Points in GeoDataFrame)
    nypoint = Point(nylon, nylat)
    helpoint = Point(hellon, hellat)
    
    # Create Great Circle Path
    gcpath = greatCirclePath(orig_point=nypoint, dest_point=helpoint)


@author: Henrikki Tenkanen, Uni. Helsinki.
"""

from shapely.geometry import Point, LineString
import numpy as np

def parseLatLon(point):
    return point.y, point.x

def coordsToLine(coords_array):
    """
    Takes an array of coordinate pair lists as input (return value of drawgreatcircle() -function) and returns a 
    Shapely LineString.
    """
    
    coordtuple_list = []
    
    # Iterate over coordinates and convert those into Shapely points         
    for coordpair in coords_array:
        # Convert coordinate list into a tuple
        coordtuple_list.append(tuple(coordpair))
        
    # Return a Shapely LineString from coordinates
    return LineString(coordtuple_list)
    
def calculateGreateCircle(orig_point, dest_point, del_s=100.0):
    # Create a Basemap instance so we can calculate GreatCirclePath
    from mpl_toolkits.basemap import Basemap
    m = Basemap()
    
    # Parse orig and dest coordinates
    olat, olon = parseLatLon(orig_point)
    dlat, dlon = parseLatLon(dest_point)
    
    # Calculate Great Circle path
    great_circle = m.drawgreatcircle(lon1=olon,lat1=olat,lon2=dlon,lat2=dlat, del_s=del_s)
    
    return great_circle
    
   
def greatCirclePath(orig_point, dest_point, del_s=100.0):
    """
    Calculates Great Circle Paths between ORIGIN and DESTINATION points. 
    
    Parameters:
    -----------
    
    orig_point: Origin point of the path. Should be passed as Shapely.Point in WGS84 projection (lat, lon).
    dest_point: Destination point of the path. Should be passed as Shapely.Point in WGS84 projection (lat, lon).
    del_s: Points on great circle computed every del_s kilometers (default 100).
    
    Returns: a Shapely.LineString 
    """
    
    # Calculate Great Circle Path
    great_circle = calculateGreateCircle(orig_point, dest_point, del_s=del_s)
    
    # Return a Shapely LineStrings from the vertices of the Great Circle line
    return coordsToLine(coords_array=great_circle.vertices)
    
def greatCircleRoute(ordered_point_list, del_s=100.0):
    """
    Calculates Great Circle Routes between multiple input Points that will be combined into a single LineString.
    The order of the points in a list determines how the lines are drawn (created in a consecutive manner).
    
    Parameters:
    -----------
    
    ordered_point_list: a list of Shapely.Point -objects in WGS84 projection. The order of the points determines how the route is formed.
    del_s: Points on great circle computed every del_s kilometers (default 100).
    
    Returns: a Shapely.LineString 
    """
    
    # Iterate over points
    for i, point in enumerate(ordered_point_list):
        
        if i == 0:
            # Take the first point as starting point (origin)
            orig_point = point
        else:
            dest_point = point
            
            # Calculate Great Circle Path between orig and dest
            great_circle = calculateGreateCircle(orig_point, dest_point, del_s=del_s)
            
            # In the first great circle calculation, initialize the route vertices array
            if i == 1:
                route_vertices = great_circle.vertices
            else:
                # Gather all vertices to route_vertices array (add to existing ones)
                route_vertices = np.concatenate((route_vertices, great_circle.vertices))
            
            # Update the orig_point to be the last point in the route
            orig_point = dest_point
    
    # Return a Shapely LineStrings from the vertices of the Great Circle line
    return coordsToLine(coords_array=route_vertices)     
      
    
def main():
    """Example how the tool can be used"""    

    # nylat, nylon are lat/lon of New York
    nylat = 40.78; nylon = -73.98
    # hellat, hellon are lat/lon of Helsinki.
    hellat = 60.17083; hellon = 24.93750
    
    # lonlat, lonlon are lat/lon of London.
    lonlat = 51.53; lonlon = 0.08
    
    # Create a Shapely Points out of the coordinates (most commonly all data are stored as Shapely Points in GeoDataFrame)
    nypoint = Point(nylon, nylat)
    helpoint = Point(hellon, hellat)
    lonpoint = Point(lonlon, lonlat)
    
    # Create Great Circle Path
    gcpath = greatCirclePath(orig_point=nypoint, dest_point=helpoint)
    
    # Create Great Circle route between multiple points
    route = [nypoint, lonpoint, helpoint, nypoint]
    gcroute = greatCircleRoute(route, del_s=100.0)
    
    return gcpath, gcroute


if __name__ == "__main__":
    great_circle_path, gcroute = main()
    

    