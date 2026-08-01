
def df_compat():
    return pd.DataFrame({"A": [1, 2, 3], "B": "foo"}, columns=pd.Index(["A", "B"]))

