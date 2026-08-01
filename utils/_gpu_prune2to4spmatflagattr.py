
def _gpu_prune2to4spmatflagattr(x, context):
    return _ods_ir.Attribute.parse(f'#gpu<prune_2to4_spmat_flag {str(x)}>', context=context)

