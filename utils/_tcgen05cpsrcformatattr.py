
def _tcgen05cpsrcformatattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.tcgen05_cp_src_fmt<{str(x)}>', context=context)

