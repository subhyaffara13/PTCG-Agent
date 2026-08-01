
def _parse_domain_op_type(domain_op: str) -> tuple[str, str]:
    split = domain_op.split("::", 1)
    if len(split) == 1:
        domain = ""
        op_type = split[0]
    else:
        domain = split[0]
        op_type = split[1]
    return domain, op_type

