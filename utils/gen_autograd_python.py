
def gen_autograd_python(
    native_functions_path: str,
    tags_path: str,
    out: str,
    autograd_dir: str,
) -> None:
    differentiability_infos, _ = load_derivatives(
        os.path.join(autograd_dir, "derivatives.yaml"), native_functions_path, tags_path
    )

    template_path = os.path.join(autograd_dir, "templates")

    # Generate Functions.h/cpp
    gen_autograd_functions_python(out, differentiability_infos, template_path)

    # Generate Python bindings
    deprecated_path = os.path.join(autograd_dir, "deprecated.yaml")
    gen_python_functions.gen(
        out, native_functions_path, tags_path, deprecated_path, template_path
    )

