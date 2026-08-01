
def _denormalmodekindattr(x, context):
    return _ods_ir.IntegerAttr.get(_ods_ir.IntegerType.get_signless(64, context=context), int(x))

