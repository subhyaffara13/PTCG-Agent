
def _tables():
    global _table_mod
    global _table_file_open_policy_is_strict
    if _table_mod is None:
        import tables

        _table_mod = tables

        # set the file open policy
        # return the file open policy; this changes as of pytables 3.1
        # depending on the HDF5 version
        with suppress(AttributeError):
            _table_file_open_policy_is_strict = (
                tables.file._FILE_OPEN_POLICY == "strict"
            )

    return _table_mod

