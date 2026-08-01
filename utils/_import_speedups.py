
def _import_speedups():
    try:
        from . import _speedups
        return (_speedups.encode_basestring_ascii,
                _speedups.encode_basestring,
                _speedups.make_encoder)
    except ImportError:
        return None, None, None

