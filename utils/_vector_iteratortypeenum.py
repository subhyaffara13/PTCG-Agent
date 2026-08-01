
def _vector_iteratortypeenum(x, context):
    return _ods_ir.Attribute.parse(f'#vector.iterator_type<{str(x)}>', context=context)

