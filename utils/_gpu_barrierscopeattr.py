
def _gpu_barrierscopeattr(x, context):
    return _ods_ir.Attribute.parse(f'#gpu.barrier_scope<{str(x)}>', context=context)

