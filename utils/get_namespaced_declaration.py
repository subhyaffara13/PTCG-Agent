
def get_namespaced_declaration(
    *,
    grouped_native_functions: Sequence[NativeFunction | NativeFunctionsGroup],
    dispatch_key: DispatchKey,
    backend_idx: BackendIndex,
    selector: SelectiveBuilder,
    rocm: bool,
    symint: bool,
) -> list[str]:
    declarations: list[str] = []
    ns_grouped_kernels: dict[str, list[str]] = defaultdict(list)
    newline = "\n"
    func = dest.RegisterDispatchKey(
        backend_idx,
        Target.NAMESPACED_DECLARATION,
        selector,
        rocm=rocm,
        class_method_name=None,
        skip_dispatcher_op_registration=False,
        symint=symint,
    )
    for f in grouped_native_functions:
        namespace = get_kernel_namespace(f=f, backend_idx=backend_idx).replace(
            "native", dispatch_key.lower()
        )

        ns_grouped_kernels[namespace].extend(
            func(f),
        )

    for namespace, kernels in ns_grouped_kernels.items():
        if len(kernels) == 0:
            continue
        ns_helper = NamespaceHelper(
            namespace_str=namespace, entity_name="", max_level=3
        )
        ordered_kernels = list(OrderedDict.fromkeys(kernels))
        declarations.extend(
            f"""
{ns_helper.prologue}
{newline.join(ordered_kernels)}
{ns_helper.epilogue}
        """.split(newline)
        )
    return declarations

