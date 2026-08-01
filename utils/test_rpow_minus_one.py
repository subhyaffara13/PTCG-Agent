
def test_rpow_minus_one(value, asarray):
    if asarray:
        value = np.array([value])
    result = value**NA

    if asarray:
        result = result[0]

    assert pd.isna(result)

