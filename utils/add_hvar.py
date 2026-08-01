
def add_HVAR(font):
    if "HVAR" in font:
        del font["HVAR"]
    axisTags = [axis.axisTag for axis in font["fvar"].axes]
    getAdvanceMetrics = partial(_get_advance_metrics, font, axisTags, HVAR_FIELDS)
    _add_VHVAR(font, axisTags, HVAR_FIELDS, getAdvanceMetrics)

