import numpy as np
import pandas as pd




def Neutron_to_Pandas(Bondlist):
    dic = dict(np.array(Bondlist).reshape(-1,2))
    dic_sorted = dict(sorted(dic.items()))# sorts the entries to give a list equally sorted acc to bond type
    df_dic = pd.DataFrame.from_dict([dic_sorted]).astype(float)
    XH_bonds = df_dic.columns
    return(df_dic, XH_bonds)

def Sort_by_euclidian_distance(x, y, list_of_parameters): # sorts the entries to give a list equally sorted acc to wrmsd and ed_value
    Zero_point_distances = []
    [Zero_point_distances.append(np.sqrt((x[i])**2 + (y[i])**2)) for i in range(len(list_of_parameters))]
    df_to_sort = pd.DataFrame({'Method': list_of_parameters, 'Zero_point_distances': Zero_point_distances})
    df_to_sort.sort_values(by=['Zero_point_distances'], inplace=True)
    return(df_to_sort['Method'].values)

def read_raw_feather(Data):# gets the raw feather files from the storage folder
    df = pd.read_feather('D:\Benchmarking\Complete_feathers' + str(Data) + '_final.feather' )
    return(df)

def EntryToDataFrame(Entry, df): # making the bond or error entry in a dataFrame to a seperate dataFrame
    GlobalEntry = [df[Entry][index].replace(':', ',').split(',')[:-1] for index in df.index]
    GlobalEntry = [dict(np.array(x).reshape(-1,2)) for x in GlobalEntry]
    GlobalEntry_sorted=[dict(sorted(x.items())) for x in GlobalEntry]
    Gdf = pd.DataFrame.from_dict(GlobalEntry_sorted).astype(float)
    return(Gdf)

def extent_Dataframe(df, header_bonds, neutronBond_dataFrame, neutronError_dataFrame):
    IAM = np.float_(df.loc[(df['Method']=='IAM'), ('R1', 'wR2','max_peak', 'max_hole', 'res_rms')].to_string(header = False, index= False).split(' '))  
    FOM = []
    wRMSD =[]
    for index, rows in df.iterrows():
        allData = [float(i) for i in [rows.R1, rows.wR2, rows.max_peak, rows.max_hole, rows.res_rms]]
        fom = [((IAM[i] - allData[i]) / IAM[i]) for i in range(len(IAM))]
        FOM.append(sum(fom))
    df.insert(8, 'FOM', FOM)

    Gdf_l = EntryToDataFrame(Entry='bondlengths', df=df)
    Gdf_e = EntryToDataFrame(Entry='bonderrors', df=df)
    Gdf_l_XH = Gdf_l[header_bonds]
    Gdf_e_XH = Gdf_e[header_bonds]

    row, col = df.shape
    
    for i in range(row):
        aa=[]
        a = np.sqrt( (neutronBond_dataFrame - Gdf_l_XH.loc[i])**2 / ((neutronError_dataFrame**2) + (Gdf_e_XH.loc[i]**2)) )
        aa.append(a)
        wRMSD.append(np.mean(aa))
    df.insert(0, 'wRMSD', wRMSD)
    

    df_not_defined = df.loc[((df['Method']=='PWLDA') | (df['Method']=='M062X')  | (df['Method']=='wB97') ) & (df['SCNL']=='True')] # Drop methods for which SCNL is not defined
    df = df.drop(list(df_not_defined.index.values))
    df = df.astype({"FOM": 'Float64'})
    df_IAM=df.loc[(df['FOM']<=0.01)]
    df = df.drop(list(df_IAM.index.values))
    df = df.dropna()
    df.reset_index(drop=True, inplace=True)
    return(df,IAM)

