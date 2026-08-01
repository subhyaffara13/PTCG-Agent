
def gen_functionalization_view_meta_classes(
    native_functions_path: str,
    tags_path: str,
    selector: SelectiveBuilder,
    install_dir: str,
    template_dir: str,
) -> None:
    from torchgen.gen import get_grouped_by_view_native_functions, parse_native_yaml

    # Parse the native_functions.yaml.
    # Then, group them into `NativeFunctionsViewGroup`.
    #
    # This is the same steps we do in gen.py (ATen codegen).
    native_functions = parse_native_yaml(
        native_functions_path, tags_path
    ).native_functions
    native_functions_with_view_groups = get_grouped_by_view_native_functions(
        native_functions
    )
    view_groups = [
        g
        for g in native_functions_with_view_groups
        if isinstance(g, NativeFunctionsViewGroup)
    ]

    fm = FileManager(install_dir=install_dir, template_dir=template_dir, dry_run=False)
    fm.write(
        "ViewMetaClassesPythonBinding.cpp",
        lambda: {
            "view_meta_bindings": list(
                concatMap(
                    lambda g: gen_functionalization_view_meta_classes_binding(
                        selector, g
                    ),
                    view_groups,
                )
            ),
        },
    )

