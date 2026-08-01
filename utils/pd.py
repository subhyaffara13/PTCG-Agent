
def pd():
    """
    Fixture to import and configure pandas. Using this fixture, the test is skipped when
    pandas is not installed. Use this fixture instead of importing pandas in test files.

    Examples
    --------
    Request the pandas fixture by passing in ``pd`` as an argument to the test ::

        def test_matshow_pandas(pd):

            df = pd.DataFrame({'x':[1,2,3], 'y':[4,5,6]})
            im = plt.figure().subplots().matshow(df)
            np.testing.assert_array_equal(im.get_array(), df)
    """
    pd = pytest.importorskip('pandas')
    try:
        from pandas.plotting import (
            deregister_matplotlib_converters as deregister)
        deregister()
    except ImportError:
        pass
    return pd

