
def test_mean_dont_convert_j_to_complex():
    # GH#36703
    df = pd.DataFrame([{"db": "J", "numeric": 123}])
    msg = r"Could not convert \['J'\] to numeric|does not support|Cannot perform"
    with pytest.raises(TypeError, match=msg):
        df.mean()

    with pytest.raises(TypeError, match=msg):
        df.agg("mean")

    msg = "Could not convert string 'J' to numeric|does not support|Cannot perform"
    with pytest.raises(TypeError, match=msg):
        df["db"].mean()
    msg = "Could not convert string 'J' to numeric|ufunc 'divide'|Cannot perform"
    with pytest.raises(TypeError, match=msg):
        np.mean(df["db"].astype("string").array)

