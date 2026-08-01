
def test_standard_norm():
    assert type(pickle.loads(pickle.dumps(mpl.colors.LogNorm()))) \
        == mpl.colors.LogNorm

