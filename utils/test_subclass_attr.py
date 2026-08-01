
def test_subclass_attr(klass):
    # testing that subclasses of ExcelWriter don't have public attributes (issue 49602)
    attrs_base = {name for name in dir(ExcelWriter) if not name.startswith("_")}
    attrs_klass = {name for name in dir(klass) if not name.startswith("_")}
    assert not attrs_base.symmetric_difference(attrs_klass)

