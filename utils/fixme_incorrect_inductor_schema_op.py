
def fixme_incorrect_inductor_schema_op(op: torch._ops.OpOverload) -> bool:
    if op.namespace != "inductor":
        return False

    # TODO - fix schema
    # Dont add any more !
    return op in (
        torch.ops.inductor.accumulate_grad_.default,
        torch.ops.inductor.resize_storage_bytes_.default,
    )

