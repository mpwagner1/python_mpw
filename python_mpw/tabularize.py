import pandas as pd


def flatten_nested_json_df(df):

    df = df.reset_index()

    # search for columns to explode/flatten
    s = (df.applymap(type) == list).any()
    list_columns = s[s].index.tolist()

    s = (df.applymap(type) == dict).any()
    dict_columns = s[s].index.tolist()

    while len(list_columns) > 0 or len(dict_columns) > 0:
        new_columns = []

        for col in dict_columns:
            # replace any null entries with empty dictionaries
            df[col] = df[col].apply(lambda x: {} if x != x else x)
            # explode dictionaries horizontally, adding new columns
            horiz_exploded = pd.json_normalize(df[col]).add_prefix(f"{col}.")
            horiz_exploded.index = df.index
            df = pd.concat([df, horiz_exploded], axis=1).drop(columns=[col])
            new_columns.extend(horiz_exploded.columns)  # inplace

        for col in list_columns:
            # replace any null entries with empty lists
            df[col] = df[col].apply(lambda x: [] if x != x else x)
            # explode lists vertically, adding new columns
            df = df.drop(columns=[col]).join(df[col].explode().to_frame())
            new_columns.append(col)

        # check if there are still dict o list fields to flatten
        s = (df[new_columns].applymap(type) == list).any()
        list_columns = s[s].index.tolist()

        s = (df[new_columns].applymap(type) == dict).any()
        dict_columns = s[s].index.tolist()

    return df.drop_duplicates()
