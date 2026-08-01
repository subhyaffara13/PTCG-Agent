
def data_test_ix(request, dirpath):
    i, test_ix = request.param
    fname = os.path.join(dirpath, f"test_sas7bdat_{i}.csv")
    df = pd.read_csv(fname)
    epoch = datetime(1960, 1, 1)
    t1 = pd.to_timedelta(df["Column4"], unit="D")
    df["Column4"] = (epoch + t1).astype("M8[s]")
    t2 = pd.to_timedelta(df["Column12"], unit="D")
    df["Column12"] = (epoch + t2).astype("M8[s]")
    for k in range(df.shape[1]):
        col = df.iloc[:, k]
        if col.dtype == np.int64:
            df.isetitem(k, df.iloc[:, k].astype(np.float64))
    return df, test_ix

