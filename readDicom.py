# WICHTIG!!! Verfahren funktioniert nur mit 
# vorkonfigurierten Bildern, deren Größe genau in mm angegeben werden müssen !!!

import pydicom
import os
import numpy
from matplotlib import pyplot, cm

# 1.) Alle DICOM-files erfassen
# Files innerhalb der Ordner sollten nach Namen sortierbar sein
PathDicom = "./sax_6/"  # Ordner in dem alle DICOM-Files liegen
lstFilesDCM = []  # Leere Liste
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # Alle DICOM-Files in die Liste aufnehmen
            lstFilesDCM.append(os.path.join(dirName,filename))

# 2.) Laden der DICOM-files
# 1st File als Refferenz
RefDs = pydicom.read_file(lstFilesDCM[0])
# Dimensionen für alle Bilder festlegen (x,y) z sei die ANzahl an Bildern
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))
# Pixel-spacing (mm) in x und y Richtung laden)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))

# 3.) Start und Stop Punkte für die Axen berechnen
x = numpy.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = numpy.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
z = numpy.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])


# 4.) RAW-Daten speichern
# Array für Dicom-Daten (Form und Datentyp) initialisieren
ArrayDicom = numpy.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

# Über alle DICOM-files 
for filenameDCM in lstFilesDCM:
    # File lesen
    ds = pydicom.read_file(filenameDCM)
    # Werte ins Array speichern
    ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array  

# 5.) Plotten des Dicom-Datensatzes
pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal', 'datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, y, numpy.flipud(ArrayDicom[:, :, 15]))
pyplot.show()