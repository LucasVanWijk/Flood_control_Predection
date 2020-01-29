# Afstroom Analyse
# Created on: 2017-06-15 14:06
# Latest version on: 09-10-2019

#################################################
# MODEL IS GETEST OP ARCMAP 10.5, HET WERKT NIET OP ARCMAP 10.2, ANDERE VERSIES ZIJN NIET GETEST.
#################################################

#################
# ESSENTIEEL
#################
#Kopieer alle folders van de kernen (met input files per kern) naar folder: D:\pStage\kernen
#Voorbeeld: in: D:\pStage\kernen\Albergen, vind je onder andere de bestanden: bk_30m_shp, bk_AHN, pandPolygon etc.
#Zorg dat dit geldt voor alle kernen die je tegelijk wilt runnen.
#################

# Import arcpy module
import arcpy
from arcpy.sa import Con
from arcpy.sa import Raster
from arcpy.sa import FocalStatistics
from arcpy.sa import IsNull
from arcpy.sa import NbrCircle
from arcpy.sa import Log10
from arcpy import env
from arcpy.sa import *
import os

arcpy.env.workspace = r"C:\Users\midni\Desktop\School\Behaviour_Based_Simulation\Utrecht_afstroomanalyse\Afstroomanalyse"
work_location = r"C:\Users\midni\Desktop\School\Behaviour_Based_Simulation\Utrecht_afstroomanalyse\Afstroomanalyse"
arcpy.env.overwriteOutput = True

arcpy.CheckOutExtension("Spatial")

#######################
# Vul in:
#######################
# Vul alle buurten in die uitgerekend moeten worden. De input files verzamelen zich per buurt in aparte folders.
# In de vorm: ['Wittevrouwen', 'Ondiep', 'etc.']
Buurten = ['Wijk_C']

# Bepaal het volume van de regenbui (in meter)
Regenbui = 0.300 # Bui volume in m
# Duur van de bui
uur = 1 # Tijd in uren
# Opname door riolering
Riool = 0.0324 # in m3/uur/m2

######################
# Model calibratie
######################
WaterdiepteStreamlines = 0.3   		#Pas deze waarde aan voor de waterhoogte op straat vanaf waar je de streamlines wil laten stromen
WaterdiepteNieuwSloten = 0.4		#Pas deze waarde aan voor de minimale waterhoogte voor de nieuwe sloten (0.4 = standaard)
MinimaleVolumeWOS = 0.10			#Pas deze waarde aan voor het minimale volume van water op straat

######################
# Model script
######################

for x in Buurten:
	arcpy.env.workspace = os.path.join(work_location, r"Buurten\{}").format(x)								# Selecteer de buurt
	arcpy.CreateFolder_management(os.path.join(work_location, r"Buurten\{}").format(x), "resultaten")		# Maak nieuwe map 'resultaten'
	arcpy.CreateFolder_management(os.path.join(work_location, r"Buurten\{}").format(x), "tijdelijk")		# Maak nieuwe map 'tijdelijk'
	
	# Verwijs naar input (zie Automatische_Selectie.py)
	BK_AHN = os.path.join(work_location, r"Buurten\{}\bk_ahn.tif").format(x)								# AHN4 tif voor de stad Utrecht					
	bk_30m_shp = os.path.join(work_location, r"Buurten\{}\bk_30m_shp.shp").format(x)						# Bebouwdekom shape 
	Wegen = os.path.join(work_location, r"Buurten\{}\Wegen_30m_shp.shp").format(x)							# Wegen shape
	
	# Clip Bebouwdekom shape naar buurt extent
	arcpy.Buffer_analysis(bk_30m_shp, os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_30m_shp_buf.shp").format(x), "100 meter", "FULL", "ROUND", "NONE")
	buf_temp = os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_30m_shp_buf.shp").format(x)
	arcpy.Clip_analysis(os.path.join(work_location, r"Input_Afstroomanalyse\pandPolygon.shp"),buf_temp ,os.path.join(work_location, r"Buurten\{}\tijdelijk\pandPolygon_clip.shp").format(x))
	
	# Output locaties nieuwe (tijdelijke) bestanden
	pandPolygon_shp = arcpy.GetParameterAsText(3)
	if pandPolygon_shp == '#' or not pandPolygon_shp:
		pandPolygon_shp = os.path.join(work_location, r"Buurten\{}\tijdelijk\pandPolygon_clip.shp").format(x) # provide a default value if unspecified
	
	Water_30m_shp = arcpy.GetParameterAsText(4)
	if Water_30m_shp == '#' or not Water_30m_shp:
		Water_30m_shp = os.path.join(work_location, r"Buurten\{}\Water_30m_shp.shp").format(x) # provide a default value if unspecified
	
	bk_zWater_30m_shp = arcpy.GetParameterAsText(7)
	if bk_zWater_30m_shp == '#' or not bk_zWater_30m_shp:
		bk_zWater_30m_shp = os.path.join(work_location, r"Buurten\{}\bk_zWater_30m_shp.shp").format(x) # provide a default value if unspecified
	
	# Rest of Script arguments	
	BK_AHN_mWmP = arcpy.GetParameterAsText(5)
	if BK_AHN_mWmP == '#' or not BK_AHN_mWmP:
		BK_AHN_mWmP = os.path.join(work_location, r"Buurten\{}\resultaten\BK_AHN_mWmP.tif").format(x) # provide a default value if unspecified
	
	BK_AHN_mW = arcpy.GetParameterAsText(17)
	if BK_AHN_mW == '#' or not BK_AHN_mW:
		BK_AHN_mW = os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_AHN_mW.tif").format(x) # provide a default value if unspecified
		
	BK_streamOrder = arcpy.GetParameterAsText(9)
	if BK_streamOrder == '#' or not BK_streamOrder:
		BK_streamOrder = os.path.join(work_location, r"Buurten\{}\resultaten\BK_streamOrder.tif").format(x) # provide a default value if unspecified
		
	BK_streamOrder_minWOS = arcpy.GetParameterAsText(9)
	if BK_streamOrder_minWOS == '#' or not BK_streamOrder_minWOS:
		BK_streamOrder_minWOS = os.path.join(work_location, r"Buurten\{}\resultaten\BK_streamOrder_minWOS.tif").format(x) # provide a default value if unspecified
		
	mpzw_strorder = arcpy.GetParameterAsText(8)
	if mpzw_strorder == '#' or not mpzw_strorder:
		mpzw_strorder = os.path.join(work_location, r"Buurten\{}\resultaten\mpzw_strorder.tif").format(x) # provide a default value if unspecified
	
	mpzw_strorder_minWOS = arcpy.GetParameterAsText(8)
	if mpzw_strorder_minWOS == '#' or not mpzw_strorder_minWOS:
		mpzw_strorder_minWOS = os.path.join(work_location, r"Buurten\{}\resultaten\pzw_strorder_minWOS.tif").format(x) # provide a default value if unspecified
		
	mPzW_fd = arcpy.GetParameterAsText(11)
	if mPzW_fd == '#' or not mPzW_fd:
		mPzW_fd = os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_fd.tif").format(x) # provide a default value if unspecified
		
	mPzW_fd_minWOS = arcpy.GetParameterAsText(11)
	if mPzW_fd_minWOS == '#' or not mPzW_fd_minWOS:
		mPzW_fd_minWOS = os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_fd_minWOS.tif").format(x) # provide a default value if unspecified
	
	outIsNull = arcpy.GetParameterAsText(12)
	if outIsNull == '#' or not outIsNull:
		outIsNull = os.path.join(work_location, r"Buurten\{}\tijdelijk\outIsNull.tif").format(x) # provide a default value if unspecified	
		
	outRgnGrp = arcpy.GetParameterAsText(12)
	if outRgnGrp == '#' or not outRgnGrp:
		outRgnGrp = os.path.join(work_location, r"Buurten\{}\tijdelijk\outRgnGrp.tif").format(x) # provide a default value if unspecified	
	
	outRgnGrp_Basin = arcpy.GetParameterAsText(12)
	if outRgnGrp_Basin == '#' or not outRgnGrp_Basin:
		outRgnGrp_Basin = os.path.join(work_location, r"Buurten\{}\tijdelijk\outRgnGrp_Basin.tif").format(x) # provide a default value if unspecified	
	
	outRgnGrp_minWOS = arcpy.GetParameterAsText(12)
	if outRgnGrp_minWOS == '#' or not outRgnGrp_minWOS:
		outRgnGrp_minWOS = os.path.join(work_location, r"Buurten\{}\tijdelijk\outRgnGrp_minWOS.tif").format(x)
		
	panden = arcpy.GetParameterAsText(13)
	if panden == '#' or not panden:
		panden = os.path.join(work_location, r"Buurten\{}\tijdelijk\panden.tif").format(x) # provide a default value if unspecified
	
	panden_0 = arcpy.GetParameterAsText(14)
	if panden_0 == '#' or not panden_0:
		panden_0 = os.path.join(work_location, r"Buurten\{}\tijdelijk\panden_0.tif").format(x) # provide a default value if unspecified
	
	Random_AHN = arcpy.GetParameterAsText(0) #Random AHN blad, om alle raster gelijk te maken
	if Random_AHN == '#' or not Random_AHN:   #Change .tif below
		Random_AHN = os.path.join(work_location, r"Buurten\{}\n_39fz1.tif").format(x) # provide a default value if unspecified
		
	resultaten = arcpy.GetParameterAsText(2)
	if resultaten == '#' or not resultaten:
		resultaten = os.path.join(work_location, r"Buurten\{}\resultaten").format(x) # provide a default value if unspecified
	
	Sloten = arcpy.GetParameterAsText(12)
	if Sloten == '#' or not Sloten:
		Sloten = os.path.join(work_location, r"Buurten\{}\tijdelijk\Sloten.tif").format(x) # provide a default value if unspecified
	
	Sloten_Int = arcpy.GetParameterAsText(12)
	if Sloten_Int == '#' or not Sloten_Int:
		Sloten_Int = os.path.join(work_location, r"Buurten\{}\tijdelijk\Sloten_Int.tif").format(x) # provide a default value if unspecified
		
	Volume_WOS = arcpy.GetParameterAsText(12)
	if Volume_WOS == '#' or not Volume_WOS:
		Volume_WOS = os.path.join(work_location, r"Buurten\{}\tijdelijk\Volume_WOS.tif").format(x)
	
	waterOpStraat = arcpy.GetParameterAsText(6)
	if waterOpStraat == '#' or not waterOpStraat:
		waterOpStraat = os.path.join(work_location, r"Buurten\{}\resultaten\waterOpStraat.tif").format(x) # provide a default value if unspecified
	
	waterVoorStreamlines = arcpy.GetParameterAsText(6)
	if waterVoorStreamlines == '#' or not waterVoorStreamlines:
		waterVoorStreamlines = os.path.join(work_location, r"Buurten\{}\resultaten\waterVoorStreamlines.tif").format(x)
	
	wos_0 = arcpy.GetParameterAsText(15)
	if wos_0 == '#' or not wos_0:
		wos_0 = os.path.join(work_location, r"Buurten\{}\resultaten\wos_0.tif").format(x) # provide a default value if unspecified
	
	water_0 = arcpy.GetParameterAsText(15)
	if water_0 == '#' or not water_0:
		water_0 = os.path.join(work_location, r"Buurten\{}\tijdelijk\water_0.tif").format(x) # provide a default value if unspecified
	
	# Lokale variabelen:
	all_basins_shape			 = os.path.join(work_location, r"Buurten\{}\tijdelijk\all_basins_shape.shp").format(x)
	all_basins_layer			 = os.path.join(work_location, r"Buurten\{}\tijdelijk\all_basins_layer.lyr").format(x)
	bk_focal					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_focal.tif").format(x)
	bk_focal2					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_focal2.tif").format(x)
	bk_focal3					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_focal3.tif").format(x)
	bk_focal4					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_focal4.tif").format(x)
	BK_max						 = os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_max.tif").format(x)
	BK_mean						 = os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_mean.tif").format(x)
	BK_min						 = os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_min.tif").format(x)
	BK_mW_NdV6					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV6.tif").format(x)
	BK_mW_NdV62					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV62.tif").format(x)
	BK_mW_NdV63					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV63.tif").format(x)
	BK_mW						 = BK_AHN
	BK_shift				     = os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_shift.tif").format(x)
	bk_zWater   	 			 = os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_zWater.tif").format(x)
	mpzw						 = os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw.tif").format(x)
	mPzW_fa						 = os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_fa.tif").format(x)
	mPzW_fa_log10				 = os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_fa_log10.tif").format(x)
	mPzW_fa_log10_minWOS	   	 = os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_fa_log10_minWOS.tif").format(x)
	mPzW_fa_minWOS				 = os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_fa_minWOS.tif").format(x)
	mpzw_fill					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_fill.tif").format(x)
	mpzw_half					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_half.tif").format(x)
	mPzW_l10_g1					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_l10_g1.tif").format(x)
	mPzW_l10_g1_minWOS			 = os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_l10_g1_minWOS.tif").format(x)
	mPzW_minWOS					 = os.path.join(work_location, r"Buurten\{}\resultaten\mPzW_minWOS.tif").format(x)
	mpzw_sinks					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_sinks.tif").format(x)
	mpzw_shift					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_shift.tif").format(x)
	mpzw_half					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_half.tif")
	outBasin					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\outBasin.tif").format(x)
	outBasin_minWOS				 = os.path.join(work_location, r"Buurten\{}\tijdelijk\outBasin_minWOS.tif").format(x)
	outIsNull					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\outisNull.tif").format(x)
	output_drop					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\output_drop").format(x)
	output_drop2				 = os.path.join(work_location, r"Buurten\{}\tijdelijk\output_drop2").format(x)
	output_drop3				 = os.path.join(work_location, r"Buurten\{}\tijdelijk\output_drop3").format(x)
	panden_max					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\panden_max.tif").format(x)
	pandPolygon_Area1			 = os.path.join(work_location, r"Buurten\{}\tijdelijk\pandPolygon_Area1").format(x)
	pandPolygon_Buffer 			 = os.path.join(work_location, r"Buurten\{}\tijdelijk\pandPolygon_Buffer").format(x)
	str_l_int					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\str_l_int.tif").format(x)
	str_l_int_minWOS			 = os.path.join(work_location, r"Buurten\{}\tijdelijk\str_l_int_minWOS.tif").format(x)
	str_l_reclass				 = os.path.join(work_location, r"Buurten\{}\tijdelijk\str_l_reclass.tif").format(x)
	str_l_reclass_minWOS		 = os.path.join(work_location, r"Buurten\{}\tijdelijk\str_l_reclass_minWOS.tif").format(x)
	Stream_lines_poly_minWOS_shp = os.path.join(work_location, r"Buurten\{}\resultaten\Stream_lines_poly_minWOS.shp").format(x)
	Stream_lines_poly_shp	     = os.path.join(work_location, r"Buurten\{}\resultaten\Stream_lines_poly.shp").format(x)
	w_complete					 = os.path.join(work_location, r"Buurten\{}\resultaten\w_complete.tif").format(x)
	w_complete_Int 				 = os.path.join(work_location, r"Buurten\{}\tijdelijk\w_complete_Int.tif").format(x)
	w_complete_shape			 = os.path.join(work_location, r"Buurten\{}\tijdelijk\w_complete_shape.shp").format(x)
	w_complete_layer			 = os.path.join(work_location, r"Buurten\{}\tijdelijk\w_complete_layer.lyr").format(x)
	w_isnull					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\w_isnull.tif").format(x)
	w_reclass					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\w_reclass.tif").format(x)
	w_reclass_shift				 = os.path.join(work_location, r"Buurten\{}\tijdelijk\w_reclass_shift.tif").format(x)
	water_full					 = os.path.join(work_location, r"Buurten\{}\resultaten\water_full.tif").format(x)
	water_min					 = os.path.join(work_location, r"Buurten\{}\resultaten\water_min.tif").format(x)
	WOS_Basins 					 = os.path.join(work_location, r"Buurten\{}\tijdelijk\WOS_Basins").format(x)
	WOS_Basins_Area				 = os.path.join(work_location, r"Buurten\{}\tijdelijk\WOS_Basins_Area.shp").format(x)
	WOS_LARGE_Basins			 = os.path.join(work_location, r"Buurten\{}\tijdelijk\WOS_LARGE_Basins.shp").format(x)
	
	#####################
	# AHN statistieken opslaan
	######################
	# Process: Zonal Statistics (3)
	arcpy.gp.ZonalStatistics_sa(bk_30m_shp, "FID", BK_AHN, BK_min, "MINIMUM", "DATA")
	
	# Process: Zonal Statistics (2)
	arcpy.gp.ZonalStatistics_sa(bk_30m_shp, "FID", BK_AHN, BK_max, "MAXIMUM", "DATA")
	
	# Process: Zonal Statistics
	arcpy.gp.ZonalStatistics_sa(bk_30m_shp, "FID", BK_AHN, BK_mean, "MEAN", "DATA")
	
	############
	#Panden naar raster en verschuiving naar correcte pixel locatie
	############	
	# Process: Polygon to Raster
	arcpy.PolygonToRaster_conversion(os.path.join(work_location, r"Buurten\{}\tijdelijk\pandPolygon_clip.shp").format(x), "FID", panden, "CELL_CENTER", "NONE", 0.5)
	
	# Process: Raster Calculator
	panden_max = Con(Raster(panden)>=0, Raster(BK_max) + 5, "")
	panden_max.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\panden_max.tif").format(x))
	
	#Process: Shif, verschuiving naar correcte pixel locatie
	arcpy.Shift_management(BK_AHN, os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_shift.tif").format(x), "0","0", panden_max)
	
	#########
	#Loop: Interpolatie van het ahn AND start stroomrichting van stroomlijnen
	#########	
	for y in range(1, 3):
		#--------water shape bewerken-------------------------------------------------------
		if y==1:
			# Process: Polygon to Raster (2)
			arcpy.PolygonToRaster_conversion(Water_30m_shp, "FID", water_full, "CELL_CENTER", "NONE", BK_AHN)
		else:
			# Process: Mosaic To New Raster (5)
			arcpy.MosaicToNewRaster_management([water_full], resultaten, "w_complete.tif", "", "32_BIT_FLOAT", "", "1", "LAST", "FIRST")
			water_full = os.path.join(work_location, r"Buurten\{}\resultaten\w_complete.tif").format(x)
		
		#--------water shape bewerken-------------------------------------------------------
		# Process: Raster Calculator (2)
		water_min = Con(Raster(water_full)>= 0, Raster(BK_min) - 0.1, "")
		water_min.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\water_min.tif").format(x))
		
		# Process: Mosaic To New Raster (2)
		arcpy.MosaicToNewRaster_management([BK_shift,water_min], resultaten, "BK_mW.tif", "", "32_BIT_FLOAT", "", "1", "MINIMUM", "FIRST")
	
		#-------Interpolating the AHN-----------------
		# Process: Raster Calculator (3) Interpolation of the raster
		out_raster = FocalStatistics(Raster(os.path.join(work_location, r"Buurten\{}\resultaten\BK_mW.tif").format(x)),NbrCircle(6,"CELL"),"MEAN","")
		out_raster.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_focal.tif").format(x))
		BK_mW_NdV6 = Con(IsNull(os.path.join(work_location, r"Buurten\{}\resultaten\BK_mW.tif").format(x)),bk_focal, Raster(os.path.join(work_location, r"Buurten\{}\resultaten\BK_mW.tif").format(x)))
		BK_mW_NdV6.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV6.tif").format(x))
	
		out_raster = FocalStatistics(Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV6.tif").format(x)),NbrCircle(6,"CELL"),"MEAN","")
		out_raster.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_focal2.tif").format(x))
		BK_mW_NdV62 = Con(IsNull(os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV6.tif").format(x)),bk_focal2, Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV6.tif").format(x)))
		BK_mW_NdV62.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV62.tif").format(x))
	
		out_raster = FocalStatistics(Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV62.tif").format(x)),NbrCircle(6,"CELL"),"MEAN","")
		out_raster.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_focal3.tif").format(x))
		BK_mW_NdV63 = Con(IsNull(os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV62.tif").format(x)),bk_focal3, Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV62.tif").format(x)))
		BK_mW_NdV63.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV63.tif").format(x))
	
		out_raster = FocalStatistics(Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV63.tif").format(x)),NbrCircle(6,"CELL"),"MEAN","")
		out_raster.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_focal4.tif").format(x))
		BK_AHN_mW = Con(IsNull(os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV63.tif").format(x)),bk_focal4, Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_mW_NdV63.tif").format(x)))
		BK_AHN_mW.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\BK_AHN_mW.tif").format(x))
	
		#--------- Adding panden to AHN after interpolation ---------------------------
		# Process: Mosaic To New Raster (3)
		arcpy.MosaicToNewRaster_management([BK_AHN_mW,panden_max], resultaten, "BK_AHN_mWmP.tif", "", "32_BIT_FLOAT", "", "1", "MAXIMUM", "FIRST")
	
		#------bk_zonder water---------------------------------------------------------------------------
		if y==1:
			# Process: Extract by Mask (2)
			# Create AHN, with waterbodies as No data points
			bk_zWater = Con(Raster(BK_AHN_mWmP)>= BK_min,1,0)
			bk_zWater.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\bk_zWater.tif").format(x))
			mpzw = SetNull(bk_zWater,BK_AHN_mWmP,"Value=0")   
			mpzw.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw.tif").format(x))
			#arcpy.gp.ExtractByMask_sa(BK_AHN_mWmP, bk_zWater_30m_shp, mpzw)
			arcpy.Shift_management(mpzw, os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_shift.tif").format(x), "0","0", panden_max)
		else:
			# Process: Is Null
			arcpy.gp.IsNull_sa(w_complete, w_isnull)
	
			# Process: Reclassify
			arcpy.gp.Reclassify_sa(w_isnull, "VALUE", "0 NODATA;1 1", w_reclass, "DATA")
			arcpy.Shift_management(w_reclass, w_reclass_shift, "0","0", panden_max)
		
			# Process: Times
			arcpy.gp.Times_sa(BK_AHN_mWmP, w_reclass_shift, mpzw_shift)
			
		# Process: Fill
		arcpy.gp.Fill_sa(mpzw_shift, mpzw_fill, "")
	
		# Process: Flow Direction
		arcpy.gp.FlowDirection_sa(mpzw_fill, mPzW_fd, "NORMAL", output_drop)
	
		# Process: Raster Calculator (5)
		mpzw_sinks = Raster(mpzw_fill) - Raster(mpzw_shift)
		mpzw_sinks.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_sinks.tif").format(x))
		
		# Process: Create raster. NoData points to 1, data points to 0
		outIsNull = IsNull(BK_AHN)
		outIsNull.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\outisNull.tif").format(x))
	
		# Process: Select 'Sloten' that are No Data point AND have a water depth of > 'WaterdiepteNieuwSloten' (defined above)
		Sloten = Con(Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\outisNull.tif").format(x))==1,Con(Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_sinks.tif").format(x))>=WaterdiepteNieuwSloten, mpzw_sinks,""))
		Sloten.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\Sloten.tif").format(x))
		
		# Process: Make interger raster for following calculations
		Sloten_Int = Int(Sloten) #Make integer
		Sloten_Int.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\Sloten_Int.tif").format(x))
	
		# Process: Create seperate groups for all 'sloten', this includes creating an attribute table
		#arcpy.gp.RegionGroup_sa(Sloten_Int, outRgnGrp, "FOUR", "WITHIN", "ADD_LINK", "")
		outRgnGrp = RegionGroup(os.path.join(work_location, r"Buurten\{}\tijdelijk\Sloten_Int.tif").format(x), "FOUR") #Create separate groups
		outRgnGrp.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\outRgnGrp.tif").format(x))
	
	######
	#Creating Water on the streets	
	######	
	# Process: Select Water on the streets, waterdepth > 0.04 (lower is neglected)
	waterOpStraat = Con(Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_sinks.tif").format(x))>= 0.04,Con(Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_sinks.tif").format(x))<= 3,mpzw_sinks,""))
	waterOpStraat.save(os.path.join(work_location, r"Buurten\{}\resultaten\waterOpStraat.tif").format(x))
	
	########
	#Creating Streamlines
	########
	# Process: Raster Calculator (10)
	wos_0 = Con(Raster(os.path.join(work_location, r"Buurten\{}\resultaten\waterOpStraat.tif").format(x))>= 0,0,"")
	wos_0.save(os.path.join(work_location, r"Buurten\{}\resultaten\wos_0.tif").format(x))
	
	# Process: Raster Calculator (11)
	panden_0 = Con(Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\panden.tif").format(x))>= 0,0,"")
	panden_0.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\panden_0.tif").format(x))
	
	# Process: Flow Accumulation
	arcpy.gp.FlowAccumulation_sa(mPzW_fd, mPzW_fa, "", "FLOAT")
	
	# Process: Raster Calculator (8)
	mPzW_fa_log10 = Log10(mPzW_fa)
	mPzW_fa_log10.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_fa_log10.tif").format(x))
		
	# Process: Raster Calculator (9)
	mPzW_l10_g1 = Con(Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_fa_log10.tif").format(x))>= 1, Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_fa_log10.tif").format(x)),"")
	mPzW_l10_g1.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_l10_g1.tif").format(x))
	
	# Process: Stream Order
	arcpy.gp.StreamOrder_sa(mPzW_l10_g1, mPzW_fd, mpzw_strorder, "STRAHLER")
	
	# Process: Raster Calculator (12)
	water_0 = Con(Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\water_min.tif").format(x))>= 0,0,"")
	water_0.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\water_0.tif").format(x))
		
	# Process: Mosaic To New Raster (4)
	arcpy.MosaicToNewRaster_management([wos_0,panden_0,mpzw_strorder,water_0], resultaten, "BK_streamOrder.tif", "", "32_BIT_FLOAT", "", "1", "MINIMUM", "FIRST")
	
	# Process: Int
	arcpy.gp.Int_sa(BK_streamOrder, str_l_int)
	
	# Process: Reclassify (2)
	arcpy.gp.Reclassify_sa(str_l_int, "VALUE", "0 NODATA;1 NODATA;2 NODATA;3 3;4 4;5 5;6 6;7 7;8 8", str_l_reclass, "DATA")
	
	# Process: Raster to Polyline
	arcpy.RasterToPolyline_conversion(str_l_reclass, Stream_lines_poly_shp, "ZERO", "0", "SIMPLIFY", "VALUE")
	
	############
	#Creating 'damaged' buildings:
	############
	# Process: Add small buffer around buildings
	arcpy.Buffer_analysis(pandPolygon_shp, os.path.join(work_location, r"Buurten\{}\tijdelijk\pandPolygon_Buffer").format(x), "0.25 Meter", "FULL", "ROUND", "NONE")
	
	# Process: Select all buildings which overlap with their buffer and the highest level of Water on the streets
	outZonalStatstable = ZonalStatisticsAsTable(os.path.join(work_location, r"Buurten\{}\tijdelijk\pandPolygon_Buffer.shp").format(x), "FID", os.path.join(work_location, r"Buurten\{}\resultaten\waterOpStraat.tif").format(x),"Table2","DATA","MAXIMUM")
	arcpy.JoinField_management(pandPolygon_shp,"FID","Table2","FID",["MAX","AREA"])
	
	# Process: Select all buildings which overlap with significant amount of water
	arcpy.MakeFeatureLayer_management(pandPolygon_shp, "pandPolygon_lyr") 
	arcpy.SelectLayerByAttribute_management("pandPolygon_lyr","NEW_SELECTION","AREA>=0.75") #Only buildings that overlap with WOS >1m2 (on the outside buffered area of the building)
	arcpy.CopyFeatures_management("pandPolygon_lyr", "pandPolygon_Area075")
	
	#Let op! Als je deze berekening meedere keren uitvoert, verwijder dan eerst 'MAX' en 'AREA' uit de attribute table van pandPolygon_shp, geldt "AREA>1" niet, want AREA wordt AREA_1
	
	############
	#Creating 'inconvience' on roads:
	############
	# Methode 1: Process: Overlast wegen, per pixel = onoverzichtelijker dan methode 2.
	Overlast_Wegen = ExtractByMask(waterOpStraat, Wegen)
	
	# Methode 2: Process: Overlast wegen, per wegdeel
	outZonalStats = ZonalStatisticsAsTable(Wegen, "id", waterOpStraat,"Table_W","DATA","MAXIMUM")
	arcpy.JoinField_management(Wegen,"id","Table_W","id",["MAX","AREA"])
	#project Wegen, properties, symbology, quantities, Max -> Classes: >0,1 ; 0,1-0,3 ; <0,3
	
	############
	#Creating Basins
	############
	#Process: Basin for completely filled DEM
	outBasin = Basin(mPzW_fd)
	outBasin.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\outBasin.tif").format(x))
	
	# Process: Create seperate groups
	outRgnGrp_Basin = RegionGroup(outBasin, "FOUR") #Create separate groups
	outRgnGrp_Basin.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\outRgnGrp_Basin.tif").format(x))
	
	# Process: Select the largest basins	
	Large_Basins = ExtractByAttributes(outRgnGrp_Basin, "Count >= 100000") #Only watersheds >100000 pixels
	Large_Basins.save(os.path.join(work_location, r"Buurten\{}\resultaten\Large_Basins.tif").format(x)) 
	
	##########
	# Streamlines to the Water Op straat for specific water depth
	##########
	#Process: Create Water on the street for a certain water depth (Defined above: 'WaterdiepteStreamlines')
	waterVoorStreamlines = Con(Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_sinks.tif").format(x))>=WaterdiepteStreamlines,mpzw_sinks,"")
	waterVoorStreamlines.save(os.path.join(work_location, r"Buurten\{}\resultaten\waterVoorStreamlines.tif").format(x))
	
	# Process: Create a partially filled AHN for the streamlines	
	mpzw_half = Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_fill.tif").format(x)) - Raster(os.path.join(work_location, r"Buurten\{}\resultaten\waterVoorStreamlines.tif").format(x))
	mpzw_half.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_half.tif").format(x)) #only contains water on the streets above 0.4
	
	# Process: Mosaic to new raster management. Creates a filled AHN up untill the defined water depth. All above this water depth is empty (and will receive streamlines)
	arcpy.MosaicToNewRaster_management([mpzw_half,mpzw_fill], resultaten, "mPzW_minWOS.tif", "", "32_BIT_FLOAT", "", "1", "FIRST", "FIRST") #Maakt een volledige hoogtekaart (daarvoor heb je mpzw_fill nodig), gevuld tot aan 0.4 en niet hoger.
	arcpy.Shift_management(mPzW_minWOS, os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_minWOSshift.tif").format(x), "0","0", panden_max)
	# Process: Create Streamlines. Same process as above.
	arcpy.gp.FlowDirection_sa(os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_minWOSshift.tif").format(x), mPzW_fd_minWOS, "NORMAL", output_drop2)
	arcpy.gp.FlowAccumulation_sa(mPzW_fd_minWOS, mPzW_fa_minWOS, "", "FLOAT") #without waterOpStraat
	mPzW_fa_log10_minWOS = Log10(mPzW_fa_minWOS)
	mPzW_fa_log10_minWOS.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_fa_log10_minWOS.tif").format(x))
	mPzW_l10_g1_minWOS = Con(Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_fa_log10_minWOS.tif").format(x))>= 1, Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_fa_log10_minWOS.tif").format(x)),"")
	mPzW_l10_g1_minWOS.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\mPzW_l10_g1_minWOS.tif").format(x))
	arcpy.gp.StreamOrder_sa(mPzW_l10_g1_minWOS, mPzW_fd_minWOS, mpzw_strorder_minWOS, "STRAHLER")
	arcpy.MosaicToNewRaster_management([wos_0,panden_0,mpzw_strorder_minWOS,water_0], resultaten, "BK_streamOrder_minWOS.tif", "", "32_BIT_FLOAT", "", "1", "MINIMUM", "FIRST")
	arcpy.gp.Int_sa(BK_streamOrder_minWOS, str_l_int_minWOS)
	arcpy.gp.Reclassify_sa(str_l_int_minWOS, "VALUE", "0 NODATA;1 NODATA;2 NODATA;3 3;4 4;5 5;6 6;7 7;8 8", str_l_reclass_minWOS, "DATA")
	arcpy.RasterToPolyline_conversion(str_l_reclass_minWOS, Stream_lines_poly_minWOS_shp, "ZERO", "0", "SIMPLIFY", "VALUE")
	
	###########
	#Creating basins, for partially filled DEM
	##########
	#Process: Create Basins (2), based on the partially filled AHN and its streamlines. Same process as above.
	outBasin_minWOS = Basin(mPzW_fd_minWOS) 
	outBasin_minWOS.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\outBasin_minWOS.tif").format(x))
	outRgnGrp_minWOS = RegionGroup(outBasin_minWOS, "FOUR") #Create separate groups
	outRgnGrp_minWOS.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\outRgnGrp_minWOS.tif").format(x))
	Large_Basins_minWOS = ExtractByAttributes(outRgnGrp_minWOS, "Count >= 100000") #Only watersheds >100000 pixels
	Large_Basins_minWOS.save(os.path.join(work_location, r"Buurten\{}\resultaten\Large_Basins_minWOS.tif").format(x))

    ################
    # Bui afhankelijkheid
    ################
	Stapgrootte = Regenbui/10
	   
	Volumes_WOS = arcpy.GetParameterAsText(12)
	if Volumes_WOS == '#' or not Volumes_WOS:
		Volumes_WOS = os.path.join(work_location, r"Buurten\{}\tijdelijk\Volumes_WOS.tif").format(x)
	   
	Volumes_Mosaic		 = os.path.join(work_location, r"Buurten\{}\tijdelijk\Volumes_Mosaic.tif").format(x)
	   
	#Create volumes	on basis of WOS
	Volumes_Mosaic = Raster(os.path.join(work_location, r"Buurten\{}\tijdelijk\mpzw_shift.tif").format(x)) + Raster(os.path.join(work_location, r"Buurten\{}\resultaten\waterOpStraat.tif").format(x))
	#Add the AHN en de WOS, bereken daarna de volumes aan de hand van het verschil. Als je dit met mpzw en mpzw_fill doet, dan krijg je ook alle WOS <0.04 
	Volumes_Mosaic.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\Volumes_Mosaic.tif").format(x))
	OutCutFill = CutFill(os.path.join(work_location, r"Buurten\{}\tijdelijk\Volumes_Mosaic.tif").format(x), mpzw_shift)	
	OutCutFill.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\OutCutFill.tif").format(x))
	#Extract volumes >0.01 m3
	Volumes_WOS = ExtractByAttributes(os.path.join(work_location, r"Buurten\{}\tijdelijk\OutCutFill.tif").format(x), "VOLUME>0.01 AND AREA>0.5") #Only areas with more than 0.50m2 water
	Volumes_WOS.save(os.path.join(work_location, r"Buurten\{}\tijdelijk\Volumes_WOS.tif").format(x))

	arcpy.RasterToPolygon_conversion(Volumes_WOS, os.path.join(work_location, r"Buurten\{}\tijdelijk\Volumes1_WOS_shp.shp").format(x), "NO_SIMPLIFY","Value")
	   
	ITERATIONS = ['Volumes1', 'Volumes2', 'Volumes3','Volumes4', 'Volumes5','Volumes6', 'Volumes7','Volumes8', 'Volumes9', 'Volumes0']
	
	_buurt = x
	   
	for x in ITERATIONS:
	#ITERATIONS
	   
		#Parameters
		Volumes1_WOS_shp		 = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_WOS_shp.shp").format(x)
		Volumes1_WOS_Points		 = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_WOS_Points.shp").format(x)
		Volumes1_points			 = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_points.tif").format(x)
		Volumes1_points_shift	 = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_points_shift.tif").format(x)
		Volumes1_Out			 = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_Out.tif").format(x)
		Volumes1_AHN			 = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_AHN.tif").format(x)
		Volumes1_fill			 = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_fill").format(x)
		Volumes1_Basin			 = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_Basin.tif").format(x)
		Volumes1_Basin_shp		 = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_Basin_shp.shp").format(x)
		Volumes1_Basin_Area		 = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_Basin_Area.shp").format(x)
		Volumes1_Intersect		 = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_Intersect.shp").format(x)
		Volumes1_Table			 = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_Table").format(x)
		Volumes1_WOS_lyr		 = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_WOS_lyr").format(x)
		
		
		Volumes1_fd = arcpy.GetParameterAsText(11)
		if Volumes1_fd == '#' or not Volumes1_fd:
			Volumes1_fd = os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_fd.tif").format(x)
	   
	   
		# Start iteration
		# Create discharge points inside (remaining) volumes.
		arcpy.FeatureToPoint_management(Volumes1_WOS_shp, Volumes1_WOS_Points, "INSIDE")
		arcpy.PointToRaster_conversion(Volumes1_WOS_Points, "Id", Volumes1_points, "COUNT", "", 0.5)
		arcpy.Shift_management(Volumes1_points, Volumes1_points_shift, "0","0", panden_max)
		Volumes1_Out = IsNull(Volumes1_points_shift)
		Volumes1_Out.save(os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_Out.tif").format(x))
		#1) Create AHN, with No data points inside every WOS volume.
		Volumes1_AHN = SetNull(Volumes1_Out,mpzw_shift,"Value=0")	  
		#2) Fill the AHN, calculate flow directions, create basins, turn to shapes to calculate area of basins.
		Volumes1_fill = arcpy.sa.Fill(Volumes1_AHN, "")
		arcpy.gp.FlowDirection_sa(Volumes1_fill, Volumes1_fd, "NORMAL", output_drop3)
		Volumes1_Basin = Basin(Volumes1_fd)
		Volumes1_Basin.save(os.path.join(work_location, r"Buurten", _buurt, r"tijdelijk\{}_Basin.tif").format(x))
		arcpy.RasterToPolygon_conversion(Volumes1_Basin, os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_Basin_shp.shp").format(x), "NO_SIMPLIFY")
		arcpy.CalculateAreas_stats(Volumes1_Basin_shp, Volumes1_Basin_Area)
		#3) Intersect the WOS with the basins to calculate the area that discharges to the Volumes of WOS
		arcpy.Intersect_analysis([os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_WOS_shp.shp").format(x),os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\{}_Basin_Area.shp").format(x)], Volumes1_Intersect, "", "", "INPUT")
		#4) Aggregate the basins of 1 Volume WOS together to get the total area that discharge to that 1 volume WOS.
		arcpy.Statistics_analysis(Volumes1_Intersect, Volumes1_Table, [["F_AREA", "SUM"]], "id")
		# Join the aggreagated table to the (remaining) WOS, calculate the total volume of water that discharges to the WOS. 
		arcpy.JoinField_management (Volumes1_WOS_shp, "id", Volumes1_Table, "id", "SUM_F_AREA")
		arcpy.AddField_management(Volumes1_WOS_shp,"{}_B".format(x),"DOUBLE")
		
		if x=='Volumes1':
			arcpy.CalculateField_management(Volumes1_WOS_shp,"{}_B".format(x),"(!SUM_F_AREA!*("+str(Stapgrootte)+" - (("+str(Riool)+"/10)*"+str(uur)+")))","PYTHON_9.3")
			arcpy.JoinField_management(Volumes1_WOS_shp, "gridcode", Volumes_WOS, "Value", "VOLUME")
			#5 Select all the Volumes that are not filled (0.9)
			arcpy.MakeFeatureLayer_management(Volumes1_WOS_shp, Volumes1_WOS_lyr)
			arcpy.SelectLayerByAttribute_management(Volumes1_WOS_lyr,"NEW_SELECTION","VOLUME*0.9>Volumes1_B")
			arcpy.CopyFeatures_management(Volumes1_WOS_lyr, os.path.join(work_location, r"Buurten", _buurt,  r"tijdelijk\Volumes2_WOS_shp.shp"))
		if x=='Volumes2':
			arcpy.CalculateField_management(Volumes1_WOS_shp,"{}_B".format(x),"(!SUM_F_AR_1!*("+str(Stapgrootte)+" - (("+str(Riool)+"/10)*"+str(uur)+")))","PYTHON_9.3")
			arcpy.JoinField_management(Volumes1_WOS_shp, "gridcode", Volumes_WOS, "Value", "VOLUME")
			#5 Select all the Volumes that are not filled (0.9)
			arcpy.MakeFeatureLayer_management(Volumes1_WOS_shp, Volumes1_WOS_lyr)
			arcpy.SelectLayerByAttribute_management(os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes2_WOS_lyr"),"NEW_SELECTION","VOLUME*0.9>(Volumes1_B+Volumes2_B)")
			arcpy.CopyFeatures_management(Volumes1_WOS_lyr, os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes3_WOS_shp.shp"))
		if x=='Volumes3':
			arcpy.CalculateField_management(Volumes1_WOS_shp,"{}_B".format(x),"(!SUM_F_AR_2!*("+str(Stapgrootte)+" - (("+str(Riool)+"/10)*"+str(uur)+")))","PYTHON_9.3")
			arcpy.JoinField_management(Volumes1_WOS_shp, "gridcode", Volumes_WOS, "Value", "VOLUME")
			#5 Select all the Volumes that are not filled (0.9)
			arcpy.MakeFeatureLayer_management(Volumes1_WOS_shp, Volumes1_WOS_lyr)
			arcpy.SelectLayerByAttribute_management(os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes3_WOS_lyr"),"NEW_SELECTION","VOLUME*0.9>(Volumes1_B+Volumes2_B+Volumes3_B)")
			arcpy.CopyFeatures_management(Volumes1_WOS_lyr, os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes4_WOS_shp.shp"))
		if x=='Volumes4':
			arcpy.CalculateField_management(Volumes1_WOS_shp,"{}_B".format(x),"(!SUM_F_AR_3!*("+str(Stapgrootte)+" - (("+str(Riool)+"/10)*"+str(uur)+")))","PYTHON_9.3")
			arcpy.JoinField_management(Volumes1_WOS_shp, "gridcode", Volumes_WOS, "Value", "VOLUME")
			#5 Select all the Volumes that are not filled (0.9)
			arcpy.MakeFeatureLayer_management(Volumes1_WOS_shp, Volumes1_WOS_lyr)
			arcpy.SelectLayerByAttribute_management(os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes4_WOS_lyr"),"NEW_SELECTION","VOLUME*0.9>(Volumes1_B+Volumes2_B+Volumes3_B+Volumes4_B)")
			arcpy.CopyFeatures_management(Volumes1_WOS_lyr, os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes5_WOS_shp.shp"))
		if x=='Volumes5':
			arcpy.CalculateField_management(Volumes1_WOS_shp,"{}_B".format(x),"(!SUM_F_AR_4!*("+str(Stapgrootte)+" - (("+str(Riool)+"/10)*"+str(uur)+")))","PYTHON_9.3")
			arcpy.JoinField_management(Volumes1_WOS_shp, "gridcode", Volumes_WOS, "Value", "VOLUME")
			#5 Select all the Volumes that are not filled (0.9)
			arcpy.MakeFeatureLayer_management(Volumes1_WOS_shp, Volumes1_WOS_lyr)
			arcpy.SelectLayerByAttribute_management(os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes5_WOS_lyr"),"NEW_SELECTION","VOLUME*0.9>(Volumes1_B+Volumes2_B+Volumes3_B+Volumes4_B+Volumes5_B)")
			arcpy.CopyFeatures_management(Volumes1_WOS_lyr, os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes6_WOS_shp.shp"))
		if x=='Volumes6':
			arcpy.CalculateField_management(Volumes1_WOS_shp,"{}_B".format(x),"(!SUM_F_AR_5!*("+str(Stapgrootte)+" - (("+str(Riool)+"/10)*"+str(uur)+")))","PYTHON_9.3")
			arcpy.JoinField_management(Volumes1_WOS_shp, "gridcode", Volumes_WOS, "Value", "VOLUME")
			#5 Select all the Volumes that are not filled (0.9)
			arcpy.MakeFeatureLayer_management(Volumes1_WOS_shp, Volumes1_WOS_lyr)
			arcpy.SelectLayerByAttribute_management(os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes6_WOS_lyr"),"NEW_SELECTION","VOLUME*0.9>(Volumes1_B+Volumes2_B+Volumes3_B+Volumes4_B+Volumes5_B+Volumes6_B)")
			arcpy.CopyFeatures_management(Volumes1_WOS_lyr, os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes7_WOS_shp.shp"))
		if x=='Volumes7':
			arcpy.CalculateField_management(Volumes1_WOS_shp,"{}_B".format(x),"(!SUM_F_AR_6!*("+str(Stapgrootte)+" - (("+str(Riool)+"/10)*"+str(uur)+")))","PYTHON_9.3")
			arcpy.JoinField_management(Volumes1_WOS_shp, "gridcode", Volumes_WOS, "Value", "VOLUME")
			#5 Select all the Volumes that are not filled (0.9)
			arcpy.MakeFeatureLayer_management(Volumes1_WOS_shp, Volumes1_WOS_lyr)
			arcpy.SelectLayerByAttribute_management(os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes7_WOS_lyr"),"NEW_SELECTION","VOLUME*0.9>(Volumes1_B+Volumes2_B+Volumes3_B+Volumes4_B+Volumes5_B+Volumes6_B+Volumes7_B)")
			arcpy.CopyFeatures_management(Volumes1_WOS_lyr, os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes8_WOS_shp.shp"))
		if x=='Volumes8':
			arcpy.CalculateField_management(Volumes1_WOS_shp,"{}_B".format(x),"(!SUM_F_AR_7!*("+str(Stapgrootte)+" - (("+str(Riool)+"/10)*"+str(uur)+")))","PYTHON_9.3")
			arcpy.JoinField_management(Volumes1_WOS_shp, "gridcode", Volumes_WOS, "Value", "VOLUME")
			#5 Select all the Volumes that are not filled (0.9)
			arcpy.MakeFeatureLayer_management(Volumes1_WOS_shp, Volumes1_WOS_lyr)
			arcpy.SelectLayerByAttribute_management(os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes8_WOS_lyr"),"NEW_SELECTION","VOLUME*0.9>(Volumes1_B+Volumes2_B+Volumes3_B+Volumes4_B+Volumes5_B+Volumes6_B+Volumes7_B+Volumes8_B)")
			arcpy.CopyFeatures_management(Volumes1_WOS_lyr, os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes9_WOS_shp.shp"))
		if x=='Volumes9':
			arcpy.CalculateField_management(Volumes1_WOS_shp,"{}_B".format(x),"(!SUM_F_AR_8!*("+str(Stapgrootte)+" - (("+str(Riool)+"/10)*"+str(uur)+")))","PYTHON_9.3")
			arcpy.JoinField_management(Volumes1_WOS_shp, "gridcode", Volumes_WOS, "Value", "VOLUME")
			#5 Select all the Volumes that are not filled (0.9)
			arcpy.MakeFeatureLayer_management(Volumes1_WOS_shp, Volumes1_WOS_lyr)
			arcpy.SelectLayerByAttribute_management(os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes9_WOS_lyr"),"NEW_SELECTION","VOLUME*0.9>(Volumes1_B+Volumes2_B+Volumes3_B+Volumes4_B+Volumes5_B+Volumes6_B+Volumes7_B+Volumes8_B+Volumes9_B)")
			arcpy.CopyFeatures_management(Volumes1_WOS_lyr, os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes0_WOS_shp.shp"))
		if x=='Volumes0':
			arcpy.CalculateField_management(Volumes1_WOS_shp,"{}_B".format(x),"(!SUM_F_AR_9!*("+str(Stapgrootte)+" - (("+str(Riool)+"/10)*"+str(uur)+")))","PYTHON_9.3")
			arcpy.JoinField_management(Volumes1_WOS_shp, "gridcode", Volumes_WOS, "Value", "VOLUME")
			#5 Select all the Volumes that are not filled (0.9)
			arcpy.MakeFeatureLayer_management(Volumes1_WOS_shp, Volumes1_WOS_lyr)
			arcpy.SelectLayerByAttribute_management(os.path.join(work_location,r"Buurten", _buurt,  r"tijdelijk\Volumes0_WOS_lyr"),"NEW_SELECTION","VOLUME*0.9>(Volumes1_B+Volumes2_B+Volumes3_B+Volumes4_B+Volumes5_B+Volumes6_B+Volumes7_B+Volumes8_B+Volumes9_B+Volumes0_B)")
			arcpy.CopyFeatures_management(Volumes1_WOS_lyr, os.path.join(work_location,r"Buurten", _buurt,  r"resultaten\Volumes0_Final.shp"))
			arcpy.AddField_management(os.path.join(work_location,r"Buurten", _buurt,  r"resultaten\Volumes0_Final.shp"),"Fill_Per","DOUBLE")
			arcpy.CalculateField_management(
				os.path.join(work_location, r"Buurten", _buurt, "resultaten\Volumes0_Final.shp"), "Fill_Per",
				"(!Volumes1_B!+!Volumes2_B!+!Volumes3_B!+!Volumes4_B!+!Volumes5_B!+!Volumes6_B!+!Volumes7_B!+!Volumes8_B!+!Volumes9_B!+!Volumes0_B!)/!Volume!*100",
				"PYTHON_9.3")
		
   		## als er tijd is: vervang de map tijdelijk in de regel hierboven door resultaten (en test!)
   		
  	
   
   ####################
   #What to select in Arcgis for overview model
   ####################
   #----In general-------
   # Select a background image: 
   # Add Data -> GIS servrs -> Add WMS: Add URL from this website: https://geodata.nationaalgeoregister.nl/luchtfoto/wms?request=GetCapabilities
   # Select 'PDOK-achtergrond luchtfoto on geodata1.nationaalgeoregister.nl'
   
   #----Water on the streets---
   # resultaten -> WaterOpStraat.tif
   # Properties -> Symbology -> light to dark blue
   
   #-----Streamlines------
   # resultaten -> Stream_lines_poly.shp (or Stream_lines_poly_minWOS.shp for partially filled AHN)
   # Properties -> Symbology -> Catagories -> Unique values. Value Field: "grid_code". Add All Values. Blue to Red
   
   #-----Buildings-------
   # Kernen -> "CITY NAME" -> pandPolygon.shp
   # Properties -> Symbology -> Hollow, with boundary = 0.2. To highlight all the locations of buildings
   # tijdelijk -> pandPolygon_Area75
   # Properties -> Symbology -> Quantaties -> Value: MAX -> yellow to red
   
   #-----Basins------
   # resultaat -> Large_Basins.shp
