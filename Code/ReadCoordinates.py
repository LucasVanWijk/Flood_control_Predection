f = open("coordinates.txt", "r")
txt = f.read()
txt = txt.split()

coordinates = []

for t in txt:
    coordinate = t.split(',')
    coordinate[0] = float(coordinate[0])
    coordinate[1] = float(coordinate[1])
    coordinates.append(coordinate)


print(coordinates)