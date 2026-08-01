
def _extract_text_encoding(encoding=None, *args, **kwargs):
    stack_level = 3
    return text_encoding(encoding, stack_level), args, kwargs


def _extract_text_encoding(encoding=None, *args, **kwargs):
    # compute stack level so that the caller of the caller sees any warning.
    is_pypy = sys.implementation.name == 'pypy'
    # PyPy no longer special cased after 7.3.19 (or maybe 7.3.18)
    # See jaraco/zipp#143
    is_old_pypi = is_pypy and sys.pypy_version_info < (7, 3, 19)
    stack_level = 3 + is_old_pypi
    return text_encoding(encoding, stack_level), args, kwargs

