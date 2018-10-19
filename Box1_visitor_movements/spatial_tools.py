import numpy as np
from scipy.spatial import cKDTree
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
from rtree import index

def buildRtree(polygon_df):
    idx = index.Index()
    for poly in polygon_df.iterrows():
        idx.insert(poly[0], poly[1]['geometry'].bounds)
    return idx

def querySpatialIndex(point, poly_df, poly_rtree, source_column):
    """Find poly containing the point"""
    # Take only x,y coordinates (only 2D dimensions implemented --> no z-value)
    point_coords = point['geometry'].coords[:][0][0:2]
    for idx_poly in poly_rtree.intersection( point_coords ):
        if poly_df['geometry'][idx_poly:idx_poly+1].values[0].contains(point['geometry']):
            return poly_df[source_column][idx_poly:idx_poly+1].values[0]
    return None

def pointInPolygon(point_df, poly_df, poly_rtree, sourceColumn_in_poly, targetColumn_in_point, fast_search=True):
    """Iterates over points"""
    data = point_df
    data[targetColumn_in_point] = None
    data[targetColumn_in_point] = point_df.apply(querySpatialIndex, axis=1, poly_df=poly_df, poly_rtree=poly_rtree, source_column=sourceColumn_in_poly)
    return data

def parseShapefilePaths(topFolder):
    paths = []
    for root, dirs, files in os.walk(topFolder):
        for filename in files:
            if filename.endswith('.shp'):
                paths.append(os.path.join(root,filename))
    return paths

def createCoordTuples(data):
    """Extracts coordinate tuples from Shapely Points objects"""
    data['xy'] = None
    for i, row in data.iterrows():
        data['xy'][i] = [np.round(row['geometry'].x, decimals=5), np.round(row['geometry'].y, decimals=5)]
    return data

def createCoordStrings(data):
    """Extracts coordinate strings from Shapely Points objects"""
    data['x'] = None
    data['y'] = None
    for i, row in data.iterrows():
        data['x'][i], data['y'][i] = "%s" % (np.round(row['geometry'].x, decimals=5)), "%s" % (np.round(row['geometry'].y, decimals=5))
    return data


def findNN(from_coords, to_coords):
    #Search nearest point from 'from_coords'
    t = cKDTree(list(from_coords['xy']))

    #Extract distance and index of closest point
    d, idx = t.query(list(to_coords['xy']), k=1) # --> k: number of nearest neighbours that are searched
    return d,idx

def CRS(inputFile):
    return inputFile.crs

def checkCrsMatch(file1, file2):
    if file1.crs == file2.crs:
        return True
    else:
        return False

def getCentroid(row, geom):
    return row[geom].centroid

def polyCentroid(df, geom_col, target_col):
    df[target_col] = None
    df[target_col] = df.apply(getCentroid, axis=1, geom=geom_col)
    return df
    
def spatialJoin(target_df, from_df, keep_all=False, **kwargs):

    #Check that files are in the same coordinate system
    if not checkCrsMatch(target_df, from_df):
        raise Exception("Input shapefiles need to be in the same coordinate system!")

    #Get columns of 'target_df'
    origColumns = list(target_df.columns)

    #Check attributes
    for a in kwargs:
        if a == 'attributes' or a == 'columns' or a == 'attr' or a == 'cols':
            attributes = kwargs[a]
            for i, col in enumerate(attributes):
                if not col in from_df.columns:
                    e = Exception("Column " + col + " does not exist in join file! Check attributes and correct spelling...\n\tAvailable attributes:" + str(list(from_df.columns)))
                    raise e

                #If the same attribute name exists also in target file, rename the attribute in join file
                if col in origColumns:
                    newname = col + "_2"
                    del attributes[i]
                    attributes.append(newname)
        else:
            raise Exception("Unknown parameter '" + a +"'.")

    #Create coordinate tuple column into dataframes
    target_df = createCoordTuples(target_df)
    from_df = createCoordTuples(from_df)

    #Find nearest neighbour's index
    dist, nnidx = findNN(from_df, target_df)

    #Create column that has index of the closest point from join_df
    target_df['nnidx'] = nnidx

    #Check join type parameter
    if keep_all:
        #joinType = 'outer' #Does not work yet!
        joinType = 'inner'
    else:
        joinType = 'inner'

    #Join attributes to target_df from join dataframe
    join = pd.merge(left=target_df, right=from_df, how=joinType, left_on='nnidx', right_index=True, suffixes=('','_2'))

    #Drop unnecessary columns from the result (i.e. coordinate tuples, nn-index, geometry the join file
    #join = join.drop(labels=['xy','xy_2', 'nnidx', 'geometry_2'], axis=1)

    #Check attributes parameter --> User can choose what attributes will be taken from the join dataframe
    if len(kwargs) == 0:
        return join
    else:
        wantedColumns = origColumns + attributes
        join = join[wantedColumns]
        return join

def main():
    #target = r"...\Target_file.shp"
    #join = r"...\Join_file.shp"

    #Read files into GeoDataFrames with geopandas
    targetFile = gpd.read_file(target)
    joinFile = gpd.read_file(join)

    #Get coordinate system of files (currently need to be in the same projection!)
    coordsys = CRS(targetFile)

    #Make spatial join between the two files
    join = spatialJoin(targetFile,joinFile) #You can choose which columns to include in the join with parameter: attributes=['attr1', 'attr2', ...]

    #Switch pandas DataFrame into geopandas GeoDataFrame
    geo = gpd.GeoDataFrame(join, geometry='geometry', crs=coordsys)

    #Save joined shapefile to disk
    #path = r"...\Joined_File.shp"
    #geo.to_file(path, driver='ESRI Shapefile')

if __name__ == "__main__":
    main()
