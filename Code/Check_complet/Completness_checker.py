#needs a method file to compare with 
#needs an (maybe) incomplete outputfile

import os
import itertools as it

from output_reader_f import open_Outputfile 

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from tkinter.simpledialog import askstring
from tkinter import messagebox
import tkinter as tk
import numpy as np
import pandas as pd
from tkinter import simpledialog

def comp_checker():
    output_folder = 'D:\Benchmarking\Completeness_checker'

    option = ['method:','basis_name:','ORCA_SCNL:','ORCA_Solvation:','becke_accuracy:','ORCA_SCF_Conv:','full_HAR:']
    opt_values = [
        ['HF',     'BP',     'B3LYP',     'R2SCAN',     'BP86',     'PWLDA',     'TPSS',     'PBE',     'PBE0',     'M062X',     'BLYP',     'wB97',     'wB97X'],
        ['STO-3G',  '3-21G', '6-31G(d)', '6-31G(d,p)', '6-311G(d,p)', '6-311++G(2d,2p)', 'cc-pVDZ', 'cc-pVTZ', 'cc-pVQZ', 'def2-SVP', 'def2-TZVP', 'def2-TZVPD', 'def2-TZVPP', 'def2-TZVPPD', 'jorge-DZP', 'jorge-TZP'],
        ["True", "False"],
        ['Vacuum', 'Water'],
        ['Normal', 'High', 'Low'],
        ['NoSpherA2SCF','SloppySCF','LooseSCF','NormalSCF','StrongSCF','TightSCF'],
        ['True']
    ]

    permutations = list(it.product(*opt_values))
    resulting_string=[]

    for index, selection in enumerate(permutations):
        line = ""
        for i,o in enumerate(option):
            if permutations[index][0] == 'M062X' and permutations[index][2] =='True':
                continue
            if permutations[index][0] == 'PWLDA' and permutations[index][2] =='True':
                continue
            if permutations[index][0] == 'wB97' and permutations[index][2] =='True':
                continue
            else:
                line += o+selection[i]+";"
            
        if line == "":
            continue
        else:
            resulting_string.append(line.rstrip(';')+'\n')

    print("We need to do "+str(len(permutations))+" calculations")

    with open(os.path.join(output_folder,'method.txt'),'w+') as f:
        f.writelines(resulting_string)
    ##### generates the needed method file to compare against #############################################
    #######################################################################################################

    df = open_Outputfile()

    vgl_list = df['wR2'].astype('float64').round(4).to_list()
    vgl_IAM = df['wR2'][ df.loc[(df['Method']=='IAM')].index[0] ]
    vgl_IAM=float(vgl_IAM)
    
    faule_Werte=[]
    mpp= [vgl_IAM-x for x in vgl_list]
    # for i,e in enumerate(mpp):
    #     if abs(e) < 0.001:
    #         faule_Werte.append(df.index[i])
   
    [faule_Werte.append(df.index[i]) for i, e  in enumerate(mpp) if abs(e) < 0.001] 

    df_temp = df.loc[(df['R1']=='0.0')]
    df=pd.concat([df, df_temp]).drop_duplicates(keep=False)
    df = df.drop(index=faule_Werte)
    ##### generates the needed pd dataframe for the next step #############################################
    #######################################################################################################
    dftoMethod = []
    for index, row in df.iterrows():
        dftoMethod.append('method:'+row['Method']+';'+'basis_name:'+row['Base']+';'+'ORCA_SCNL:'+row['SCNL']+';'+'ORCA_Solvation:'+row['Solvent']+';'+'becke_accuracy:'+row['Becke Accuracy']+';'+'ORCA_SCF_Conv:'+row['SCF Conv']+';full_HAR:True')
    #print(dftoMethod)  

    original_method = set([line.strip() for line in open('D:\Benchmarking\Completeness_checker\method.txt', 'r+')])


    dftoMethod = set(dftoMethod)
    m=[]
    missing = list(sorted(original_method-dftoMethod))
    for index,el in enumerate(missing):
        m.append(el+'\n')

    with open(os.path.join(output_folder,'Arg_16_02.txt'),'w+') as f:
        f.writelines(m)

if __name__ == '__main__':
    comp_checker()

