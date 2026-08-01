
def _gpu_prune2to4spmatflag(x, context):
    return _ods_ir.IntegerAttr.get(_ods_ir.IntegerType.get_signless(32, context=context), int(x))

