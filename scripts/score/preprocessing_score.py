#!/bin/python3
# coding: utf-8

""" Select, clean and merge score dataset from camcan directory. """

# libraries
import os
import pandas as pd

# path
path_data = "/home/mehdi/data/camcan/cc700-scored"


def get_df(path):
    """
    Function to extract a df from the text files
    : param path: string
    : return: dataframe, list of integers
    """
    size = os.path.getsize(path)
    if size == 0:
        return None, None
    l = []
    with open(path, mode="rt", encoding="utf-8") as f:
        i = 0
        for row in f:
            if "-----------------------------------------" in row:
                l.append(i)
            i += 1
    if len(l) == 0:
        df = pd.read_csv(path, engine="python", sep="\t")
        l = [0, i]
    elif len(l) == 1:
        df = pd.read_csv(path, skiprows=l[0]+1, sep="\t")
        l = [l[0], i]
    elif len(l) == 2:
        df = pd.read_csv(path, skiprows=l[0]+1, skipfooter=i-l[1], engine="python", sep="\t")
        l = [l[0], l[1]]
    elif len(l) >= 3:
        df = pd.read_csv(path, skiprows=l[1]+1, skipfooter=i-l[2], engine="python", sep="\t")
        l = [l[1], l[2]]
    else:
        return None, l
    return df, l


def check_unicity(df, index):
    """
    Function to validate and clean the dataframe
    : param df: dataframe
    : param index: string (column to check)
    : return: dataframe
    """
    # check unicity
    l = []
    for i in df[index]:
        test = df.query("%s == '%s'" % (index, i))
        if len(test) != 1:
            l.append(i)
    df = df.query("%s not in %s" % (index, str(l)))
    return df


def clean_df(df, index):
    """
    Function to clean the dataframe
    : param df: dataframe
    : param index: string (column to check)
    : return: dataframe
    """
    idx = []
    for i in df.index:
        if "ErrorMessages" in df.columns:
            if df.at[i, "ErrorMessages"] != df.at[i, "ErrorMessages"] or df.at[i, "ErrorMessages"] in ["0.00000", "None", " "]:
                idx.append(i)
        elif "ErrorMessage" in df.columns:
            if df.at[i, "ErrorMessage"] != df.at[i, "ErrorMessage"] or df.at[i, "ErrorMessage"] in ["0.00000", "None", " "]:
                idx.append(i)
        else:
            idx.append(i)
    col = [c for c in df.columns if c not in ["ErrorMessages", "ErrorMessage"]]
    return df.ix[idx, col]

# participants
path_participants = os.path.join(path_data, "participant_data.csv")
big_df = pd.read_csv(path_participants)
print("number of participants :", big_df.shape[0], "\n")

# merge data
d = {}
for i in os.listdir(path_data):
    print(i)
    path0 = os.path.join(path_data, i)
    if os.path.isdir(path0):
        path1 = os.path.join(path0, "release001")
        if os.path.isdir(path1):
            path2 = os.path.join(path1, "summary")
            if os.path.isdir(path2):
                for j in os.listdir(path2):
                    if "summary" in j and "with_ages" not in j:
                        path_df = os.path.join(path2, j)
                        df, l = get_df(path_df)
                        if df is not None:
                            d[i] = path_df
        path1bis = os.path.join(path0, "release002")
        if os.path.isdir(path1bis):
            path2 = os.path.join(path1bis, "summary")
            if os.path.isdir(path2):
                for j in os.listdir(path2):
                    if "summary" in j and "with_ages" not in j:
                        path_df = os.path.join(path2, j)
                        df, l = get_df(path_df)
                        if df is not None:
                            d[i+"bis"] = path_df
print("\n")
for key in d:
    df, _ = get_df(d[key])
    index = df.columns[0]
    df = check_unicity(df, index)
    df = clean_df(df, index)
    print(df.shape, key)
    big_df = big_df.merge(df, how="left", left_index=True, left_on="Observations", right_on=index)
big_df.reset_index(drop=True, inplace=True)
print("\n")
print("total shape :", big_df.shape)

# save results
path = os.path.join(path_data, "total_score.csv")
print("output :", path)
big_df.to_csv(path, sep=";", encoding="utf-8", index=False)
