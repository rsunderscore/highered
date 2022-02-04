# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 14:18:45 2022

@author: Rob
"""
import pandas as pd
import zipfile
from io import StringIO
import numpy as np
#import yaml #pyyaml
SPECIALNULL = 'PrivacySuppressed'
ZIPNAME = r'ignoredir/CollegeScorecard_Raw_Data_08032021.zip'


def get_col_info(datadf, colname, colsource = 'source', map='all'):
    """Search a data dictionary dataframe fror a column
    return close matches

    Parameters
    ----------
    datadf : dataframe, 
        the dataframe that has dictionary columns.
    colname : str
        the column name to search for.
    colsource : str, optional
        the column to search [source, or sourcep_]. The default is 'source'.
    map : str, optional
        filter on map column ['program', 'all']. The default is 'all'.

    Returns
    -------
    ret : DataFrame
        dictionary rows for columns that are close matches to the provided text.

    """
    #get info about a column
    ret= datadf[datadf[colsource].str.contains(colname, flags=2).fillna(False)]
    if map=='program':
        ret = ret[ret['map'] == 'program']
    return ret

def df_from_zipcsv(zipname, csvname, specialnull = SPECIALNULL, specialnull_fill = "-1"):
    typdict = {'OPEID': str, 'ZIP':str, 'ALIAS':str, 'CIPTITLE2':str, 'CIPTITLE3':str, 'CIPTITLE4':str,
           'SEPAR_DT_MDN': str,'REPAY_DT_MDN': str, 'T4APPROVALDATE': str,
           'NPCURL': str,'CIPTITLE5':str, 'CIPTITLE6':str,
          }
    s = read_file_from_zip(zipname, csvname).decode().replace(specialnull, specialnull_fill)
    df = pd.read_csv(StringIO(s), dtype=typdict)
    #df['filename'] = csvname
    return df

def get_csv_from_zipfile(zipname, csvname):
    with zipfile.ZipFile(zipname) as z:
        df = pd.read_csv(z.open(csvname))
    return df

def read_file_from_zip(zipname, fname):
    if isinstance(zipname, zipfile.ZipFile):
        zipname = zipname.filename
        
    z= zipfile.ZipFile(zipname)
    f = z.open(fname).read()
    z.close()
    return f

def load_excel(f):
    """
    Load all sheets as dataframes from an excel file.

    Parameters
    ----------
    f : string
        filename to read.

    Returns
    -------
    resdict : dictionary mapping sheetnames to the df from that sheet

    """
    e = pd.ExcelFile(f, engine='openpyxl')
    resdict = {}
    for n in e.sheet_names:
        resdict[n] = e.parse(n)
    print(f"loaded {len(resdict)} sheets from f")
    e.close()
    return resdict

def yaml_to_df(lines, keyfield='name'):
    """
    Custom parsing of yaml file from data.gov scorecard dataset

    Parameters
    ----------
    lines : a list of lists (lines split by colon separator)
    keyfield : string, optional
        the field that starts a new set of entries. The default is 'name'.

    Returns
    -------
    pandas DataFrame
        columns are field labels and values are rows

    """
    fl = []
    curdict = {}
    for f in lines:
        if len(f)<1: continue
        if keyfield in f[0]: 
            #flush the old dict
            if len(curdict) > 0: 
                fl.append(curdict)
            #start a new dict
            curdict = {}     
            curdict[keyfield] = f[1]
        else:
            try:
                curdict[f[0].strip()] = f[1].strip()
            except IndexError as e:
                print(e)
                print(f)
    return pd.DataFrame(fl)

