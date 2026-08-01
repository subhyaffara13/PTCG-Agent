
def get_native_function_declarations_from_ns_grouped_kernels(
    *,
    ns_grouped_kernels: dict[str, list[str]],
) -> list[str]:
    declarations: list[str] = []
    newline = "\n"
    for namespace, kernels in ns_grouped_kernels.items():
        ns_helper = NamespaceHelper(
            namespace_str=namespace,
            entity_name="",
            max_level=4,
        )
        # Convert to a set first to remove duplicate kernel names. Backends are
        # allowed to repeat kernel names; only generate the declaration once!
        ordered_kernels = list(OrderedDict.fromkeys(kernels))
        declarations.extend(
            f"""
{ns_helper.prologue}
{newline.join(ordered_kernels)}
{ns_helper.epilogue}
        """.split(newline)
        )
    return declarations

