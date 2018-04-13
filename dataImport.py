import pydicom as dicom     # Read DICOM Files
import os            # Directory File-ops
import pandas as pd  # JUst for CSV-Files

data_dir = ''
patients = os.listdir(data_dir)
labels_df = pd.read_csv('.csv', index_col=0)

labels_df.head()

for patient in patients[:1]:
    label = labels_df.get_value(patient, 'cancer', 'cancer')
    path = data_dir + patient
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x : int(int(x.ImagePositionPatient[2])))
    print(len(slices), label)
    print(slices[0])