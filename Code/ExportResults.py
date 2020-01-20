import arcpy

# IMPORTANT: voeg in je code workspace het volgende toe:
# Folder 'Results', hierin voeg je het volgende toe:
# Folder 'PNG'
# Folder 'Simulations'
# Folder 'Templates', hier voeg je een leeg .mxd bestand toe (open ArcMap, leeg bestand, sla deze op in 'Templates')

workspace = r"C:\Users\midni\Desktop\School\Behaviour_Based_Simulation\Code\Results\\" # Wijzig naar het Path waar je code zich bevind
results = r"C:\Users\midni\Desktop\School\Behaviour_Based_Simulation\Utrecht_afstroomanalyse\Afstroomanalyse\Buurten\Wijk_C\resultaten\\" # Wijzig naar het Path waar de resultaten van de simulatie zich bevinden

# Unittest: voor deze code is het niet mogelijk om een echte Unit test uit te voeren
# Om toch te testen of het werkt: check in je workspace folder de folder 'PNG'. Als je daarin een png bestand ziet,
# die dezelfde naam heeft als je ingevoerde fileName, dan werkt de code.
def exportPNG(file, fileName):
    mxd = arcpy.mapping.MapDocument(file)
    arcpy.mapping.ExportToPNG(mxd, workspace+r"PNG\\"+fileName+".png")
    del mxd

# Test: wanneer je zeker weet dat exportPNG werkt kan je testen of addLayers ook werkt.
# Dit doe je als volgt: open het png bestand dat je net hebt gemaakt. Vind nu het ArcMap bestand die je gebruikt hebt
# voor de png. Open dit bestand in ArcMap. Vergelijk of alle toegevoegde layers in ArcMap overeen komen met degene die je
# in het png bestand ziet.
def addLayers(path):
    mxd = arcpy.mapping.MapDocument(path)
    df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
    addLayer = arcpy.mapping.Layer(results+"WOS_na_bui.tif")
    arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")

    mxd.save()
    del mxd

# Test: wanneer beide addLayers en exportPNG werken kan je testen of exportResults ook werkt
# Dit doe je als volgt: controleer eerst of er in je Templates folder daadwerkelijk een *leeg* .mxd (ArcMap) bestand staat.
# Check vervolgens of er in de folder 'Simulations' ook daadwerkelijk een .mxd bestand wordt aangemaakt met dezelfde naam als je
# ingevoerde fileName. Als dit allemaal klopt kan je als laatste controle nog checken of er een juist png bestand wordt aangemaakt
# met layers die overeenkomen met de daadwerkelijke layers in ArcMap 
def exportResults(fileName):
    mxd = arcpy.mapping.MapDocument(workspace+r"Templates\template.mxd")
    pathMXD = workspace+r"Simulations\\" + fileName + ".mxd"
    mxd.saveACopy(pathMXD)
    addLayers(pathMXD)
    exportPNG(pathMXD, fileName)



exportResults("testSimulation13")