
def _fproundingmodeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.fp_rnd_mode<{str(x)}>', context=context)

