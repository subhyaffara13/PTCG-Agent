
def _add_VVAR(font, masterModel, master_ttfs, axisTags):
    getAdvanceMetrics = partial(
        _get_advance_metrics, font, masterModel, master_ttfs, axisTags, VVAR_FIELDS
    )
    _add_VHVAR(font, axisTags, VVAR_FIELDS, getAdvanceMetrics)

