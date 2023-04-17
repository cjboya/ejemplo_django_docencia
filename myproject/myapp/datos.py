f = open("aeropuertos.csv", encoding="utf8")
datos = f.readlines()
f.close()

for n in datos:
    aux = n.split(",")
    aeropuerto =  aux[1].replace('"', "")
    ciudad =  aux[2].replace('"', "")
    pais =  aux[3].replace('"', "")
# print(datos)
