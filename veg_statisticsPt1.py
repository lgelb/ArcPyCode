import os
import arcpy
from arcpy import env
from arcpy.sa import *

# Set Geoprocessing environments
arcpy.env.cellSize = "MINOF"
arcpy.env.workspace = r'C:\Users\Lucy\Documents\GISthings\DCEW_VegStatistics\bufferedWSveg.gdb'

dem = r'C:\Users\Lucy\Documents\GISthings\DCEW_VegStatistics\miscrasters\bare1m.gdb\DEM_coarseres'

# create and store aspect
outAspect = Aspect(dem)

'''set up vegetation rasters'''
pftVeg = r'C:\Users\Lucy\Documents\GISthings\DCEW_VegStatistics\veg_4classes'
# raster of n and s aspects
veg_n = Con((outAspect < 45) | (outAspect > 315), pftVeg)
veg_s = Con((outAspect < 225) & (outAspect > 135), pftVeg)

''' buffer around weather stations '''
# load pointfile of weather stations that will be buffered
featureToBuffer = r'C:\Users\Lucy\Documents\GISthings\DCEW_VegStatistics\bufferedWSveg.gdb\DCEW_WS4'
distance = 1000
distanceField = "{} meters".format(distance)
# creates shapefile of buffers (outBuffer)
# if you get an error here, try restarting computer to release schema lock
arcpy.Buffer_analysis(featureToBuffer, 'outBuffer', distanceField)

'''Execute PolygonToRaster of buffers'''
valField = 'Field1'
assignmentType = "MAXIMUM_AREA"
priorityField = 'Field4'
cellSize = 0.00001  # 0.000001
# creates raster (outRaster) of the buffer shapefile
arcpy.PolygonToRaster_conversion('outBuffer', valField, 'outRaster', assignmentType, priorityField, cellSize)
