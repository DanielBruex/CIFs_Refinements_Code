

def read_output_file(path, keys=['method', 'basis_name', 'ORCA_Solvation', 'becke_accuracy', 'ORCA_SCF_Conv', 'SCNL', 'Weight', 'Nr. NPD', 'R1_gt', 'wR2','goof', 'max_peak', 'max_hole', 'res_rms', 'bondlengths', 'bonderrors']):
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
                            if key == 'bondlengths'or key == 'bonderrors':
                                result_list[i].append(l.split('\t')[1])
                            elif key =="basis_name" or key == "max_peak":
                                result_list[i].append(v.split(":")[2])
                            else:
                                result_list[i].append(v.split(":")[1])
            else:
                pass
    for i, key in enumerate(keys):
        if len(result_list[i])!= max([len(x) for x in result_list]):
            result_list[i].append('IAM')
            #result_list[i].insert(0, 'IAM')
        else:
            pass
    return result_list


