
def test_use_bottleneck():
    if nanops._BOTTLENECK_INSTALLED:
        with pd.option_context("use_bottleneck", True):
            assert pd.get_option("use_bottleneck")

        with pd.option_context("use_bottleneck", False):
            assert not pd.get_option("use_bottleneck")

