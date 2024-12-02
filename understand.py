import understand

db = understand.open("C:/Users/sif/Desktop/mgl869/mgl869.und")
for file in db.ents("file"):
   print(file.longname())