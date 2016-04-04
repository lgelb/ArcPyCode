import arcpy
from arcpy import env
from arcpy.sa import *

arcpy.env.workspace = r'C:\Users\Lucy\Documents\GISthings\LandlabvsDCEW\NS100xsyntheticDEM.gdb'
solar_rad = r'C:\Users\Lucy\Documents\GISthings\LandlabvsDCEW\NS100xsyntheticDEM.gdb\solar_rad'
dem = r'C:\Users\Lucy\Documents\GISthings\LandlabvsDCEW\NS100xsyntheticDEM.gdb\topoDEM_NS_d100x'

# create and store aspect
outAspect = Aspect(dem)
outAspect.save('aspect')

''' find radiation by aspect '''
rad_n = Con((outAspect < 45) | (outAspect > 315), solar_rad)
rad_n = Int(rad_n)
arcpy.BuildRasterAttributeTable_management(rad_n)
rad_n.save('rad_north')

rad_s = Con((outAspect < 225) & (outAspect > 135), solar_rad)
rad_s = Int(rad_s)
arcpy.BuildRasterAttributeTable_management(rad_s)
rad_s.save('rad_south')

'''save north to csv'''
arcpy.env.workspace = r'C:\Users\Lucy\Documents\GISthings\LandlabvsDCEW'
outfile = open('rad_north.csv', "w")
# make a list of the fields
fieldList = arcpy.ListFields(rad_n)
# write the header (field names) using list comprehension
outfile.write(",".join(['"' + field.name + '"' for field in fieldList]) + "\n")
# open a search cursor
searchRows = arcpy.SearchCursor(rad_n)
# loop through the rows
for searchRow in searchRows:
    # write out the field values of each row using list comprehension
    outfile.write(",".join([str(searchRow.getValue(field.name))
                            for field in fieldList]) + "\n")
# delete the cursor objects
del searchRow, searchRows
# close file
outfile.close()

'''save south to csv'''
outfile = open('rad_south.csv', "w")
# make a list of the fields
fieldList = arcpy.ListFields(rad_s)
# write the header (field names) using list comprehension
outfile.write(",".join(['"' + field.name + '"' for field in fieldList]) + "\n")
# open a search cursor
searchRows = arcpy.SearchCursor(rad_s)
# loop through the rows
for searchRow in searchRows:
    # write out the field values of each row using list comprehension
    outfile.write(",".join([str(searchRow.getValue(field.name))
                            for field in fieldList]) + "\n")
# delete the cursor objects
del searchRow, searchRows
# close file
outfile.close()

# elev constraints: ("bare1m_fill" > 1070) & ("bare1m_fill" < 1170)
