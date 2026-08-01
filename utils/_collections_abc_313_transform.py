
def _collections_abc_313_transform() -> nodes.Module:
    """See https://github.com/python/cpython/pull/124735"""
    return AstroidBuilder(AstroidManager()).string_build(
        "from _collections_abc import *"
    )

