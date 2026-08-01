
def _gpu_transposemodeattr(x, context):
    return _ods_ir.Attribute.parse(f'#gpu<mat_transpose_mode {str(x)}>', context=context)

