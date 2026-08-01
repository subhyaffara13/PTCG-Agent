
def _gpu_shufflemodeattr(x, context):
    return _ods_ir.Attribute.parse(f'#gpu<shuffle_mode {str(x)}>', context=context)

