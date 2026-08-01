
def add_VVAR(font):
    if "VVAR" in font:
        del font["VVAR"]
    getAdvanceMetrics = partial(_get_advance_metrics, font, axisTags, VVAR_FIELDS)
    axisTags = [axis.axisTag for axis in font["fvar"].axes]
    _add_VHVAR(font, axisTags, VVAR_FIELDS, getAdvanceMetrics)

