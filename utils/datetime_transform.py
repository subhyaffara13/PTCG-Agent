
def datetime_transform() -> nodes.Module:
    """The datetime module was C-accelerated in Python 3.12, so use the
    Python source."""
    return AstroidBuilder(AstroidManager()).string_build("from _pydatetime import *")

