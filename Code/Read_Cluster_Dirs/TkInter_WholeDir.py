from tkinter import *
from tkinter.ttk import *
from tkinter.simpledialog import askstring
import os
import numpy as np
import pandas as pd
from tkinter import filedialog
from tkinter import messagebox

import output_reader_wholeDir


def Opendir():
    root = Tk()
    root.withdraw()
    emptylist=[]
    b=0
    df=pd.DataFrame(emptylist)
    file_path = filedialog.askdirectory()
    for file in os.listdir(file_path):
             print(b)
             #result = np.array(output_reader_wholeDir.read_output_file(path= os.path.join(file_path, file) , keys=['method', 'basis_name', 'ORCA_Solvation', 'becke_accuracy', 'ORCA_SCF_Conv', 'SCNL', 'Weight', 'R1_gt', 'wR2','goof', 'max_peak', 'max_hole', 'res_rms']))  
             result = np.array(output_reader_wholeDir.read_output_file(path= os.path.join(file_path, file) , keys=['method', 'basis_name', 'ORCA_Solvation', 'becke_accuracy', 'ORCA_SCF_Conv', 'SCNL', 'Weight', 'Nr. NPD', 'R1_gt', 'wR2','goof', 'max_peak', 'max_hole', 'res_rms', 'bondlengths', 'bonderrors'])).T 
             df_temp = pd.DataFrame(result,columns=['Method', 'Base', 'Solvent', 'Becke Accuracy', 'SCF Conv', 'SCNL', 'weight',  'Nr. NPD', 'R1', 'wR2', 'Goof', 'max_peak', 'max_hole', 'res_rms', 'bondlengths', 'bonderrors'])
             df = pd.concat([df, df_temp], ignore_index=True)
             df = df.drop_duplicates(subset=('Method', 'Base', 'Solvent', 'Becke Accuracy', 'SCF Conv', 'SCNL', 'weight'))
             b +=1
    struc = askstring('Structure', 'Name Your Data')
    df.insert(0, 'Data', struc)
    df = df.replace({'6-311G(d' : '6-311G(d,p)', '6-311++G(2d' : '6-311++G(2d,2p)', '6-31G(d'  : '6-31G(d,p)'})##new
    summary = df.value_counts('Method').to_string()
    messagebox.showinfo('Summary', summary)
    df.to_feather(os.path.join(struc + '.feather'))
    return(df, struc, summary)

a= Opendir()


        
