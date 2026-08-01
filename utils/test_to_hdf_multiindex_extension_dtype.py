
def test_to_hdf_multiindex_extension_dtype(idx, temp_h5_path):
    # GH 7775
    mi = MultiIndex.from_arrays([idx, idx])
    df = DataFrame(0, index=mi, columns=["a"])
    with pytest.raises(NotImplementedError, match="Saving a MultiIndex"):
        df.to_hdf(temp_h5_path, key="df")

