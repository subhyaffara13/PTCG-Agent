
def _tensormapl2promokind(x, context):
    return _ods_ir.IntegerAttr.get(_ods_ir.IntegerType.get_signless(32, context=context), int(x))

