
def _materialize_cpp_cia_ops() -> None:
    """
    Utility function to query C++ dispatcher to get the all
    possible CIA ops and populate them into torch.ops namespace
    """
    cia_ops = torch._C._dispatch_get_registrations_for_dispatch_key(
        "CompositeImplicitAutograd"
    )

    # Materialize all CIA ops
    for op in cia_ops:
        namespace, op_name = tuple(op.split("::"))
        split_list = op_name.split(".")
        # Sometime overload could be missing
        if len(split_list) not in (1, 2):
            raise AssertionError(f"expected 1 or 2 parts, got {len(split_list)}")
        op_name = split_list[0]
        op_overload_name = "default"
        if len(split_list) == 2:
            op_overload_name = split_list[1]

        _ = getattr(getattr(getattr(torch.ops, namespace), op_name), op_overload_name)

