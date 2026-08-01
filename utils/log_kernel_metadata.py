
def log_kernel_metadata(
    kernel_name: str, kernel_path: str, kernel_module_code: str
) -> None:
    """
    An utility to log kernel metadata. We may parse metadata from kernel source code here.

    It's fine to parse the generated kernel code here since the logging is
    disabled by default. It would hurt compilation time.
    """
    from .wrapper_benchmark import get_kernel_category_by_source_code

    kernel_category = get_kernel_category_by_source_code(kernel_module_code)
    reduction_hint = _parse_reduction_hint(kernel_category, kernel_module_code)
    size_hints = _parse_size_hints(kernel_module_code, kernel_category)
    kernel_fn_code = _parse_kernel_fn_code(kernel_module_code)

    proper_kernel_fn_code = _parse_proper_kernel_fn_code(kernel_fn_code)

    # the line of code excluding the decortors
    kernel_line_of_code = _parse_kernel_line_of_code(proper_kernel_fn_code)

    get_metric_table("kernel_metadata").add_row(
        lambda: {
            "kernel_name": kernel_name,
            "kernel_path": kernel_path,
            "kernel_category": kernel_category,
            "size_hints": size_hints,
            "reduction_hint": reduction_hint,
            "line_of_code": kernel_line_of_code,
            "num_load": _count_pattern(proper_kernel_fn_code, "tl.load"),
            "num_store": _count_pattern(proper_kernel_fn_code, "tl.store"),
            "num_for_loop": _count_pattern(proper_kernel_fn_code, "for "),
            "num_atomic_add": _count_pattern(proper_kernel_fn_code, "tl.atomic_add"),
            "num_args": _count_args(proper_kernel_fn_code),
            "xnumel": _parse_numel(proper_kernel_fn_code, "xnumel"),
            "ynumel": _parse_numel(proper_kernel_fn_code, "ynumel"),
            "rnumel": _parse_numel(proper_kernel_fn_code, "rnumel"),
            "kernel_args_num_gb": _parse_kernel_args_num_gb(
                kernel_fn_code, kernel_category
            ),
        }
    )

