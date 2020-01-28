# This code has executed in the python console in arcMap. If executed in pycharm licenses should be explicitly verified.
# The code is executed on "Wijk_C"

import arcpy
import matplotlib.pyplot as plt
import os
arcpy.CheckOutExtension("Spatial")



buurt='Wittevrouwen'
path='C:/Users/tom_s/Desktop/afstroomanalyse/Utrecht_afstroomanalyse/Afstroomanalyse'
#folder waar point file wordt opgeslagen
outPoint_path='C:/Users/tom_s/Documents/ArcGIS/Default.gdb'


def raster_to_point():
    inRaster = r'{}/Buurten/{}/bk_ahn.tif'.format(path,buurt)

    outPoint = r'{}/RasterT_tif12'.format(outPoint_path)
    field = "VALUE"

    arcpy.env.overwriteOutput = True
    arcpy.RasterToPoint_conversion(inRaster, outPoint, field)


# updateCursor updates all given points to the given height the raster file.
def updateCursor(begin_coordinates,end_coordinates,new_height):
    begin_x, begin_y = begin_coordinates
    end_x, end_y = end_coordinates
    fc=r'{}/RasterT_tif12'.format(outPoint_path)
    with arcpy.da.UpdateCursor(fc,["SHAPE@XY","grid_code"]) as cursor:
        for point in cursor:
            coordinates=point[0]
            if end_x>coordinates[0]>begin_x and end_y>coordinates[1]>begin_y:
                point[1]=new_height
                # point.setValue("grid_code", new_height)
                cursor.updateRow(point)
                # break is used, so it changes only one point. Just to check if updating works.


def point_to_raster():
    inRaster = r'{}/Buurten/{}/bk_ahn.tif'.format(path,buurt)
    fc=r'{}/RasterT_tif12'.format(outPoint_path)
    arcpy.PointToRaster_conversion(fc, "grid_code", inRaster, "MAXIMUM", "", inRaster)

def change_dir_name(end_string1,end_string2):
    fn ='{}/Buurten/{}'.format(path,buurt+end_string1)
    new_fn='{}/Buurten/{}'.format(path,buurt+end_string2)
    os.rename(fn,new_fn)

# default folder is wijk_c. This is without changes. Now e need to convert wijk_c - kopie to default to make changes
change_dir_name("", "2")
change_dir_name(" - kopie", "")


# make changes
# convert tif file to points with values of the height
raster_to_point()

# # Update points in new raster ('RasterT_tif'). First one is for wijk_c, second one for wittevrouwen.
# updateCursor((136000,456200),(136400,456900),6)
updateCursor((137270,456700),(137380,456800),-5)

point_to_raster()




