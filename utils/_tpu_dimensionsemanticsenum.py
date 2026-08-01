
def _tpu_dimensionsemanticsenum(x, context):
    return _ods_ir.Attribute.parse(f'#tpu.dimension_semantics<{str(x)}>', context=context)

