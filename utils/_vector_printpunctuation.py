
def _vector_printpunctuation(x, context):
    return _ods_ir.Attribute.parse(f'#vector.punctuation<{str(x)}>', context=context)

