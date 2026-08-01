
def _collect_all_valid_cia_ops_for_namespace(
    op_namespace: torch._ops._OpNamespace,
) -> set["OperatorBase"]:
    # Step 1: Materialize all ops from C++ dispatcher
    _materialize_cpp_cia_ops()

    # Step 2: Query all ops from python dispatcher
    cia_ops = set()
    for op in op_namespace:
        op_packet = getattr(op_namespace, op)
        for overload in op_packet.overloads():
            op_overload = getattr(op_packet, overload)
            if _is_preservable_cia_op(op_overload):
                cia_ops.add(op_overload)
    return cia_ops

