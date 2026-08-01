
def combine_selective_builders(
    lhs: SelectiveBuilder, rhs: SelectiveBuilder
) -> SelectiveBuilder:
    include_all_operators = lhs.include_all_operators or rhs.include_all_operators
    debug_info = merge_debug_info(lhs._debug_info, rhs._debug_info)
    operators = merge_operator_dicts(lhs.operators, rhs.operators)
    kernel_metadata = merge_kernel_metadata(lhs.kernel_metadata, rhs.kernel_metadata)
    et_kernel_metadata = merge_et_kernel_metadata(
        lhs.et_kernel_metadata, rhs.et_kernel_metadata
    )
    include_all_non_op_selectives = (
        lhs.include_all_non_op_selectives or rhs.include_all_non_op_selectives
    )
    custom_classes = lhs.custom_classes.union(rhs.custom_classes)
    build_features = lhs.build_features.union(rhs.build_features)
    return SelectiveBuilder(
        include_all_operators,
        debug_info,
        operators,
        kernel_metadata,
        et_kernel_metadata,
        custom_classes,
        build_features,
        include_all_non_op_selectives,
    )

