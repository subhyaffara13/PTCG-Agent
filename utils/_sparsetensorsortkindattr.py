
def _sparsetensorsortkindattr(x, context):
    return _ods_ir.Attribute.parse(f'#sparse_tensor<SparseTensorSortAlgorithm {str(x)}>', context=context)

