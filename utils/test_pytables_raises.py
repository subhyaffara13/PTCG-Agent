
def test_pytables_raises(temp_h5_path):
    df = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(ImportError, match="tables"):
        df.to_hdf(temp_h5_path, key="df")

