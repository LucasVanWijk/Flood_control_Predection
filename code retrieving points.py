# This code has executed in the python console in arcMap. If executed in pycharm licenses should be explicitly verified.
# The code is executed on "Wijk_C"

import arcpy

arcpy.CheckOutExtension("Spatial")

# path waar bk_ahn.tif file in staat
arcpy.env.workspace = r'C:\Users\tom_s\Desktop\afstroomanalyse\Utrecht_afstroomanalyse\Afstroomanalyse\Buurten\Wijk_C'
tif_workspace = r'C:\Users\tom_s\Documents\ArcGIS\Default.gdb'
# Raster name (last number could be different after multiple runs)
tif_file = 'RasterT_tif12'

# Change raster to points
# Define raster file and point file
inRaster = r'C:\Users\tom_s\Desktop\afstroomanalyse\Utrecht_afstroomanalyse\Afstroomanalyse\Buurten\Wijk_C\bk_ahn.tif'
outPoint = tif_workspace + "\\" + tif_file
field = "VALUE"

# enables to save on same file
arcpy.env.overwriteOutput = True

# Execute RasterToPoint
arcpy.RasterToPoint_conversion(inRaster, outPoint, field)

fc = outPoint

# Enable editor
edit = arcpy.da.Editor(tif_workspace)


# updateCursor updates all given points to the given height the raster file.
def updateCursor(begin_coordinates,end_coordinates,new_height):
    begin_x, begin_y = begin_coordinates
    end_x, end_y = end_coordinates
    with arcpy.da.UpdateCursor(fc,["SHAPE@XY","grid_code"]) as cursor:
        for point in cursor:
            coordinates=point[0]
            if end_x>coordinates[0]>begin_x and end_y>coordinates[1]>begin_y:
                point[1]=new_height
                # point.setValue("grid_code", new_height)
                cursor.updateRow(point)
                # break is used, so it changes only one point. Just to check if updating works.


# # Define all data/points of 'bk_ahn.tif'
data=arcpy.da.SearchCursor(fc,["SHAPE@XY","grid_code"])
# # Update points in new raster ('RasterT_tif')
updateCursor((136000,456300),(136100,456400),50)


arcpy.PointToRaster_conversion(fc, "grid_code", outPoint, "MAXIMUM" , "", inRaster)






