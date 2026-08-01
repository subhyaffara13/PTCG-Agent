
def _gpu_allreduceoperationattr(x, context):
    return _ods_ir.Attribute.parse(f'#gpu<all_reduce_op {str(x)}>', context=context)

