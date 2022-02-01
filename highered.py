# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 14:18:45 2022

@author: Rob
"""
import pandas as pd
#import yaml #pyyaml


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

