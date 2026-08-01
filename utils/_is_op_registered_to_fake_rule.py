
def _is_op_registered_to_fake_rule(op: OpOverload) -> bool:
    return op in op_implementations_dict

