
def set_generic_fs(protocol, **storage_options):
    """Populate the dict used for method=="generic" lookups"""
    _generic_fs[protocol] = filesystem(protocol, **storage_options)

