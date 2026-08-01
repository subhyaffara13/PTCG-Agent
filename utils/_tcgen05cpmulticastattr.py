
def _tcgen05cpmulticastattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tcgen05_cp_multicast<{str(x)}>', context=context)

