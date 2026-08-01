
def _tcgen05cpshapeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tcgen05_cp_shape<{str(x)}>', context=context)

