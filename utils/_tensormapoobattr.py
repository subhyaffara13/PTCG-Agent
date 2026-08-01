
def _tensormapoobattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvgpu<oob {str(x)}>', context=context)

