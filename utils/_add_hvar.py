
def _add_HVAR(font, masterModel, master_ttfs, axisTags):
    getAdvanceMetrics = partial(
        _get_advance_metrics, font, masterModel, master_ttfs, axisTags, HVAR_FIELDS
    )
    _add_VHVAR(font, axisTags, HVAR_FIELDS, getAdvanceMetrics)

