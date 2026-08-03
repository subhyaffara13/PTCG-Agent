from typing import List, Tuple, Union

def _dispatch_index_op_fold_results(
    ofrs: Sequence[Union[Operation, OpView, Value, int]],
) -> Tuple[List[Value], List[int]]:
    """`mlir::dispatchIndexOpFoldResults`"""
    dynamic_vals = []
    static_vals = []
    for ofr in ofrs:
        if isinstance(ofr, (Operation, OpView, Value)):
            val = _get_op_result_or_value(ofr)
            dynamic_vals.append(val)
            static_vals.append(ShapedType.get_dynamic_size())
        else:
            static_vals.append(ofr)
    return dynamic_vals, static_vals

