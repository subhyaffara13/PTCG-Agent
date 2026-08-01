
def _memscopekindattr(x, context):
    return _ods_ir.Attribute.parse(f'#nvvm.mem_scope<{str(x)}>', context=context)

