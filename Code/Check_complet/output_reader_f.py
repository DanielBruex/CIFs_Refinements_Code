import os
import itertools as it
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from tkinter.simpledialog import askstring
from tkinter import messagebox
import os
import tkinter as tk
import numpy as np
import pandas as pd
from tkinter import simpledialog
def read_output_file(path, keys=['R1_gt', "wR2", "goof",'basis_name', 'method']):
    result_list = []
    for key in keys:
        result_list.append([])
    
    with open (path, 'rt') as file:
        for line in file:
            l = line.strip("\n")
            if "CIF-stats" in l:
                continue
            if any(key in l for key in keys):
                if key == 'Weight':
                    values = l.split(',')
                else:
                    values = l.split('\t')
                    values = l.split(',')
                for v in values:
                    for i,key in enumerate(keys):
                        if key in v:
                            if key =="basis_name" or key == "max_peak":
                                result_list[i].append(v.split(":")[2])
                            else:
                                result_list[i].append(v.split(":")[1])
            else:
                pass
    for i, key in enumerate(keys):
        if len(result_list[i])!= len(result_list[-2]):
            result_list[i].insert(0, 'IAM')
        else:
            pass
    return result_list

def open_Outputfile():
    root = Tk() #creates an instance for tkinter window or frame
    root.geometry('300x300') #sets geometry
    file = askopenfile(mode ='r', filetypes =[('Text Files', '*.txt'), ('Feather Files', '*.feather')])
    
    if file:
        filepath = os.path.abspath(file.name)
        extension = filepath.split('.')[-1]
    
        if extension == 'txt':
            result = np.array(read_output_file(path= filepath, keys=['method', 'basis_name', 'ORCA_Solvation', 'becke_accuracy', 'ORCA_SCF_Conv', 'SCNL', 'Weight', 'R1_gt', 'wR2','goof', 'max_peak', 'max_hole', 'res_rms'])).T    
            df = pd.DataFrame(result,columns=['Method', 'Base', 'Solvent', 'Becke Accuracy', 'SCF Conv', 'SCNL', 'weight', 'R1', 'wR2', 'Goof', 'max_peak', 'max_hole', 'res_rms'])
            df = df.drop_duplicates(subset=('Method', 'Base', 'Solvent', 'Becke Accuracy', 'SCF Conv', 'SCNL', 'weight'))
            df = df.replace({'6-311G(d' : '6-311G(d,p)', '6-311++G(2d' : '6-311++G(2d,2p)', '6-31G(d'  : '6-31G(d,p)'})
    
        else:
            df = pd.read_feather(filepath)
            df = df.replace({'6-311G(d' : '6-311G(d,p)', '6-311++G(2d' : '6-311++G(2d,2p)', '6-31G(d'  : '6-31G(d,p)'})
    
    

    return(df)

