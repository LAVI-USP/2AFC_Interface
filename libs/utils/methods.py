
import pathlib
import pydicom
import numpy as np
import os
from distutils.dir_util import copy_tree


def filesep():
    """Check the system and use / or \\"""
    
    if os.name == 'posix':
        return '/'
    else:
        return '\\'

path2read_real = 'data{}images{}real'.format(filesep(), filesep())
path2read_simu = 'data{}images{}simu'.format(filesep(), filesep())


def readDicom(path):
    
    dcmFiles = [str(item) for item in pathlib.Path(path).glob("*.dcm") if '._' not in str(item)]
    
    # Test if list is empty
    if not dcmFiles: 
        a=1
        raise ValueError('No DICOM files found in the specified path.')
    
    slices = [None] * len(dcmFiles)
    
    nSlices = []
    for f in dcmFiles:
        nSlices.append(int(f.split(filesep())[-1].split('.')[0]))
    offset = np.min(nSlices)    
    
    
    for f in dcmFiles:
        nSlice = int(f.split(filesep())[-1].split('.')[0])
        slices[nSlice - offset] = pydicom.dcmread(f, force=True).pixel_array
    
    slices = np.stack(slices, axis=-1).astype(np.uint16)
    
    return slices


def find_simu_rois():
    
    # List all patients    
    patient_cases = [str(item) for item in pathlib.Path(path2read_simu).glob("*{}**{}recon_contrast_*".format(filesep(),filesep())) if pathlib.Path(item).is_dir()]


    return patient_cases

def find_real_rois():
    
    # List all patients    
    patient_cases = [str(item) for item in pathlib.Path(path2read_real).glob("*{}**".format(filesep())) if item.is_dir() and ('CC' in str(item) or 'MLO' in str(item))]

    
    return patient_cases

# def copy_rois(cases, path2write):
    
#     # Create the destination dir
#     if not os.path.exists(path2write_real):
#         os.makedirs(path2write_real)
        
#     for case in cases:
#         copy_tree(case, "{}/{}".format(path2write, '/'.join(case.split('/')[-1:-5:-1][-1::-1])))


if __name__ == '__main__':
    
    path2read_real = '..{}..{}data{}images{}real'.format(filesep(), filesep(), filesep(), filesep())
    path2read_simu = '..{}..{}data{}images{}simu'.format(filesep(), filesep(), filesep(), filesep())
    
    patient_cases_simu = find_simu_rois()
    
    patient_cases_real = find_real_rois()
            
    # path2write_real = "/home/rodrigo/Dropbox/ROIs/real"
    # path2write_simu = "/home/rodrigo/Dropbox/ROIs/simu"
    
    # copy_rois(patient_cases_simu, path2write_simu)
    # copy_rois(patient_cases_real, path2write_real)
    


    
    
    