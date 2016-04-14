import os
import arcpy
from arcpy import env
from arcpy.sa import *

arcpy.env.workspace = r'C:\Users\Lucy\Documents\GISthings\DCEW_VegStatistics\bufferedWSveg.gdb'
dem = r'C:\Users\Lucy\Documents\GISthings\DCEW_VegStatistics\miscrasters\bare1m_fl_int'
pftVeg = r'C:\Users\Lucy\Documents\GISthings\DCEW_VegStatistics\veg_4classes'

# create and store aspect
outAspect = Aspect(dem)
# raster of n and s aspects
veg_n = Con((outAspect < 45) | (outAspect > 315), pftVeg)
veg_s = Con((outAspect < 225) & (outAspect > 135), pftVeg)

''' buffer around weather stations '''
featureToBuffer = r'C:\Users\Lucy\Documents\GISthings\DCEW_VegStatistics\bufferedWSveg.gdb\DCEW_WS_4' 
outBuffer = r'C:\Users\Lucy\Documents\GISthings\DCEW_VegStatistics\bufferedWSveg.gdb\buff50m'
distanceField = "50 meters"
# creates shapefile of buffers
# if you get an error here, try restarting computer to release schema lock
arcpy.Buffer_analysis(featureToBuffer, outBuffer, distanceField)

# Execute PolygonToRaster of buffers
valField = 'Field1'
outRaster = r'C:\Users\Lucy\Documents\GISthings\DCEW_VegStatistics\bufferedWSveg.gdb\buf50m_raster'
assignmentType = "MAXIMUM_AREA"
priorityField = 'Field4'
cellSize = 0.00001 # 0.000001
arcpy.PolygonToRaster_conversion(outBuffer, valField, outRaster, assignmentType, priorityField, cellSize)
outRaster = Lookup(Raster(outRaster), 'Field1')

# changes out of sys32 directory to create a txt file
mydir = r'C:\Users\Lucy\Documents\GISthings\DCEW_VegStatistics'
os.chdir(mydir)
arcpy.env.workspace = mydir

#creates a csv
outfile = open('veg_byWS.csv', "w")
# loop through 5 weather stations, find veg n and s, save to csv
for i in range(1,5):
    temp_n = Con(outRaster == i, veg_n)
    temp_s = Con(outRaster == i, veg_s)
    print('finished temp aspect files')
    # title saying which weather station
    outfile.write("weather station,{}\n".format(i))

    # specify north aspect
    outfile.write("north aspect")
    # make a list of the fields
    fieldList = arcpy.ListFields(temp_n)
    # write the header (field names) using list comprehension
    outfile.write(",".join(['"' + field.name + '"' for field in fieldList]) + "\n")
    # open a search cursor
    searchRows = arcpy.SearchCursor(temp_n)
    # loop through the rows
    for searchRow in searchRows:
        # write out the field values of each row using list comprehension
        outfile.write(",".join([str(searchRow.getValue(field.name))
                                for field in fieldList]) + "\n")
    # delete the cursor objects
    del searchRow, searchRows

    # specify south aspect
    outfile.write("south aspect")
    # make a list of the fields
    fieldList = arcpy.ListFields(temp_s)
    # write the header (field names) using list comprehension
    outfile.write(",".join(['"' + field.name + '"' for field in fieldList]) + "\n")
    # open a search cursor
    searchRows = arcpy.SearchCursor(temp_s)
    # loop through the rows
    for searchRow in searchRows:
        # write out the field values of each row using list comprehension
        outfile.write(",".join([str(searchRow.getValue(field.name))
                                for field in fieldList]) + "\n")
    # delete the cursor objects
    del searchRow, searchRows

    # add visual space
    outfile.write("\n")

# close file
outfile.close()


'''unused code'''

#    temp.save('veg_n_ws{}'.format(i))
#        arcpy.SelectLayerByAttribute_management(outBuffer, "NEW_SELECTION", ['Field1'] = ws)
# Perform some action with row[1] (i.e. the point geometry)
# elev constraints: ("bare1m_fill" > 1070) & ("bare1m_fill" < 1170)
# with arcpy.da.SearchCursor(outBuffer, "Field1") as cursor:
