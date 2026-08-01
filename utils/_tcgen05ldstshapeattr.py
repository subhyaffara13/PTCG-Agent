
def _tcgen05ldstshapeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tcgen05_ldst_shape<{str(x)}>', context=context)

