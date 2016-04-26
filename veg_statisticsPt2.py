'''start finding veg by ws'''
# changes out of sys32 directory to create a txt file
mydir = r'C:\Users\Lucy\Documents\GISthings\DCEW_VegStatistics'
os.chdir(mydir)
arcpy.env.workspace = mydir

#creates a csv
outfile = open('veg_byWS{}meters.csv'.format(distance), "w")

# loop through 5 weather stations, find veg n and s, save to csv

for i in range(1,5):
    expr=r'Con("Outraster"==%i,"veg_n")'%i    
    temp_n = arcpy.gp.Rastercalculator(expr)
    expr=r'Con("Outraster"==%i,"veg_s")'%i    
    temp_s = arcpy.gp.Rastercalculator(expr)

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