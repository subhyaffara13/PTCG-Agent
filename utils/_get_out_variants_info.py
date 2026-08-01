
def _get_out_variants_info(functional_op) -> str:
    """Collect information about overloads tagged with out_variant for debugging."""
    namespace = functional_op.namespace
    op_name = functional_op._schema.name.split("::")[1]
    torch_packet = getattr(getattr(torch.ops, namespace), op_name)

    overloads_info: list[str] = []
    for overload_name in torch_packet.overloads():
        candidate = getattr(torch_packet, overload_name)
        # pyrefly: ignore [missing-attribute]
        if torch.Tag.out_variant in candidate.tags:
            overloads_info.append(f"  - {overload_name}: {candidate._schema}")

    return "\n".join(overloads_info)

