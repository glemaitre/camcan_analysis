#!/bin/python3
# coding: utf-8

""" Select, clean and merge score dataset from camcan directory. """

# libraries
import os
import pandas as pd
import json
print("\n")

# path
path_data = "/home/arthur/arthur_imbert/dev/cc700-scored"


def get_df(path):
    """
    Function to extract a df from the text files
    : param path: string
    : return: dataframe, list of integers
    """
    size = os.path.getsize(path)
    if size == 0:
        return None
    l = []
    with open(path, mode="rt", encoding="utf-8") as f:
        i = 0
        for row in f:
            if "-----------------------------------------" in row:
                l.append(i)
            i += 1
    if len(l) == 0:
        df = pd.read_csv(path, engine="python", sep="\t")
    elif len(l) == 1:
        df = pd.read_csv(path, skiprows=l[0]+1, sep="\t")
    elif len(l) == 2:
        df = pd.read_csv(path, skiprows=l[0]+1, skipfooter=i-l[1],
                         engine="python", sep="\t")
    elif len(l) >= 3:
        df = pd.read_csv(path, skiprows=l[1] + 1, skipfooter=i - l[2],
                         engine="python", sep="\t")
        df = df[df.columns[:2]]
        for j in range(len(l)):
            if j % 2 == 1:
                start = l[j] + 1
                end = i - l[j + 1]
                df_part = pd.read_csv(path, skiprows=start, skipfooter=end,
                                      engine="python", sep="\t")
                _class = df_part.at[0, df_part.columns[1]].strip()
                header = ["_".join([_class, c]) for c in df_part.columns]
                df_part.columns = header
                df = df.merge(df_part, how="left", left_index=True,
                              left_on="CCID", right_on=df_part.columns[0])
        header = [c for c in df.columns if c != df.columns[1]
                  and "ErrorMessages" not in c]
        df = df[header]
    else:
        return None
    return df


def check_unicity(df, col_index):
    """
    Function to validate and clean the dataframe
    : param df: dataframe
    : param col_index: string (column to check)
    : return: dataframe
    """
    # check unicity
    l = []
    for i in df[col_index]:
        test = df.query("%s == '%s'" % (col_index, i))
        if len(test) != 1:
            l.append(i)
    df = df.query("%s not in %s" % (col_index, str(l)))
    return df


def clean_df(df):
    """
    Function to clean the dataframe
    : param df: dataframe
    : return: dataframe
    """
    idx = []
    for i in df.index:
        if "ErrorMessages" in df.columns:
            if df.at[i, "ErrorMessages"] != df.at[i, "ErrorMessages"] \
                    or df.at[i, "ErrorMessages"] in ["0.00000", "None", " "]:
                idx.append(i)
        elif "ErrorMessage" in df.columns:
            if df.at[i, "ErrorMessage"] != df.at[i, "ErrorMessage"] \
                    or df.at[i, "ErrorMessage"] in ["0.00000", "None", " "]:
                idx.append(i)
        else:
            idx.append(i)
    col = [c for c in df.columns if c not in ["ErrorMessages", "ErrorMessage"]]
    return df.ix[idx, col]


def merge_data(path_data, filename_participants):
    """
    Function to merge the different datasets
    :param path_data: string
    :param filename_participants: string
    :return: dataframe, dictionary
    """
    d = {}
    d_features = {}
    for i in os.listdir(path_data):
        path0 = os.path.join(path_data, i)
        if os.path.isdir(path0):
            path1 = os.path.join(path0, "release001")
            if os.path.isdir(path1):
                path2 = os.path.join(path1, "summary")
                if os.path.isdir(path2):
                    for j in os.listdir(path2):
                        if "summary" in j and "with_ages" not in j:
                            path_df = os.path.join(path2, j)
                            df = get_df(path_df)
                            if df is not None:
                                d[i] = path_df
            path1bis = os.path.join(path0, "release002")
            if os.path.isdir(path1bis):
                path2 = os.path.join(path1bis, "summary")
                if os.path.isdir(path2):
                    for j in os.listdir(path2):
                        if "summary" in j and "with_ages" not in j:
                            path_df = os.path.join(path2, j)
                            df = get_df(path_df)
                            if df is not None:
                                d[i + "bis"] = path_df
    path_participants = os.path.join(path_data, filename_participants)
    big_df = pd.read_csv(path_participants)
    col_to_delete = [c for c in big_df.columns if c != "Observations"]
    print("merging datasets...")
    for key in d:
        df = get_df(d[key])
        index = df.columns[0]
        df = check_unicity(df, index)
        df = clean_df(df)
        print(df.shape, key)
        d_features[key] = tuple(list(df.columns))
        big_df = big_df.merge(df, how="left", left_index=True,
                              left_on="Observations", right_on=index)
    print("\n")
    big_df = big_df[[c for c in big_df.columns if c not in col_to_delete]]
    big_df.reset_index(drop=True, inplace=True)
    return big_df, d_features

# merge data
big_df, d_features = merge_data(path_data, "participant_data.csv")
print("total shape :", big_df.shape, "\n")

# save results
path = os.path.join(path_data, "total_score.csv")
print("output data :", path)
big_df.to_csv(path, sep=";", encoding="utf-8", index=False)
path = os.path.join(path_data, 'behavioural_features.json')
print("output features :", path)
with open(path, 'w') as f:
    json.dump(d_features, f)

