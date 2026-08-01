
def _gpu_broadcasttypeattr(x, context):
    return _ods_ir.Attribute.parse(f'#gpu<broadcast {str(x)}>', context=context)

