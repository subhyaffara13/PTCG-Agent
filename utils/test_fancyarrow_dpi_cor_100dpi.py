
def test_fancyarrow_dpi_cor_100dpi():
    """
    Check the export of a FancyArrowPatch @ 100 DPI. FancyArrowPatch is
    instantiated through a dedicated function because another similar test
    checks a similar export but with a different DPI value.

    Remark: test only a rasterized format.
    """

    __prepare_fancyarrow_dpi_cor_test()

