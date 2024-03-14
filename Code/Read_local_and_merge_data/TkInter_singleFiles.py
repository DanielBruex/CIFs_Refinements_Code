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

import output_reader


# This function will be used to open a SISYPHOS-Output (txt)file and return it as (Pandas) DataFrame according to the given keys and dimensions (columns) 
def open_Outputfile():
    root = Tk() #creates an instance for tkinter window or frame
    root.geometry('300x300') #sets geometry
    file = askopenfile(mode ='r', filetypes =[('Text Files', '*.txt'), ('Feather Files', '*.feather')])
    
    if file:
        filepath = os.path.abspath(file.name)
        extension = filepath.split('.')[-1]
    
        if extension == 'txt':
            result = np.array(output_reader.read_output_file(path= filepath, keys=['method', 'basis_name', 'ORCA_Solvation', 'becke_accuracy', 'ORCA_SCF_Conv', 'SCNL', 'Weight', 'Nr. NPD', 'R1_gt', 'wR2','goof', 'max_peak', 'max_hole', 'res_rms', 'bondlengths', 'bonderrors'])).T    
            df = pd.DataFrame(result,columns=['Method', 'Base', 'Solvent', 'Becke Accuracy', 'SCF Conv', 'SCNL', 'weight',  'Nr. NPD','R1', 'wR2', 'Goof','max_peak', 'max_hole', 'res_rms', 'bondlengths', 'bonderrors'])

    
        else:
            df = pd.read_feather(filepath)
            df=df.drop(['Data'], axis=1)
    

    return(df, filepath)


def number_files():
    num_files = simpledialog.askinteger('Number of files to be summed up', 'Enter number of files')
    return(num_files)


#small function needs an input to be added as first row for a new txt file 
def structure_name():
    struc = askstring('Structure', 'Name Your Data')
    return(struc)

def conv_toFeather(df):
    conv_box = messagebox.askquestion('Convert DataFrame to Feather?')
    if conv_box == 'yes':
        df.to_feather()#hier jetzt irgendwie den outputnamen für die feather datei einbringen



def summary():
    summary = df.value_counts('Method').to_string()
    messagebox.showinfo('Summary', summary)
    


DataFiles=[]
if len(DataFiles) == 0:
    num_files = number_files()
    df, filepath = open_Outputfile()
    DataFiles.append(filepath)
    if num_files >= 0:   
        for i in range(num_files-1):
            df_new, filepath_new = open_Outputfile()
            DataFiles.append(filepath_new)
            df = pd.concat([df, df_new], ignore_index=True)
            df = df.replace({'6-311G(d' : '6-311G(d,p)', '6-311++G(2d' : '6-311++G(2d,2p)', '6-31G(d'  : '6-31G(d,p)'})
            df = df.drop_duplicates(subset=('Method', 'Base', 'Solvent', 'Becke Accuracy', 'SCF Conv', 'SCNL'), keep='last')
            
            if i == num_files - 2:
                b = summary()
            else:
                continue    
    else:
        pass
else:
    pass

#print(df)

struc = structure_name()
df.insert(0, 'Data', struc)

df.to_feather(os.path.join('Pro_final.feather'))



# for another window below can be used
# from Tkinter_tests import open_Outputfile

# p = open_Outputfile()
# print(p)
