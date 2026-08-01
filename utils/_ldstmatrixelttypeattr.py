
def _ldstmatrixelttypeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.ld_st_matrix_elt_type<{str(x)}>', context=context)

