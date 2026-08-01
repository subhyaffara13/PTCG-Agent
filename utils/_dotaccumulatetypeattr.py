
def _dotaccumulatetypeattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.dot_accumulate_type<{str(x)}>', context=context)

