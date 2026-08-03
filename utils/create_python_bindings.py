from typing import Callable

def create_python_bindings(
    fm: FileManager,
    pairs: Sequence[PythonSignatureNativeFunctionPair],
    pred: Callable[[NativeFunction], bool],
    module: str | None,
    filename: str,
    *,
    method: bool,
    symint: bool = True,
) -> None:
    """Generates Python bindings to ATen functions"""
    py_methods: list[str] = []
    ops_headers: list[str] = []
    py_method_defs: list[str] = []
    py_forwards: list[str] = []

    grouped = group_filter_overloads(pairs, pred)

    for name in sorted(grouped.keys(), key=str):
        overloads = grouped[name]
        py_methods.append(
            method_impl(name, module, overloads, method=method, symint=symint)
        )
        py_method_defs.append(method_def(name, module, overloads, method=method))
        py_forwards.extend(forward_decls(name, overloads, method=method))
        ops_headers.append(f"#include <ATen/ops/{name.base}.h>")

    fm.write_with_template(
        filename,
        filename,
        lambda: {
            "generated_comment": "@"
            + f"generated from {fm.template_dir_for_comments()}/{filename}",
            "ops_headers": ops_headers,
            "py_forwards": py_forwards,
            "py_methods": py_methods,
            "py_method_defs": py_method_defs,
        },
    )

