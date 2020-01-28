import matplotlib.pyplot as plt

buurt="Wittevrouwen"
path="C:/Users/tom_s/Desktop/afstroomanalyse/Utrecht_afstroomanalyse/Afstroomanalyse"

def show_tif():
    waterstand_zonder_verandering = path+"/Buurten/"+buurt+"/resultaten/WS_na_bui.tif"
    img = plt.imread(waterstand_zonder_verandering)
    plt.imshow(img[:, :, 0], cmap=plt.cm.coolwarm)
    plt.show()
    return img

try:
    exec (open(path+"/Afstroomanalyse_Model.py").read())
    exec(open(path+"/Script ralf.py").read())
except Exception as e:
    print(e)

# show waterlevel
waterlevel=show_tif()


