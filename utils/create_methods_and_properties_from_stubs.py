
def create_methods_and_properties_from_stubs(
    concrete_type, method_stubs, property_stubs
) -> None:
    method_defs = [m.def_ for m in method_stubs]
    method_rcbs = [m.resolution_callback for m in method_stubs]
    method_defaults = [get_default_args(m.original_method) for m in method_stubs]

    property_defs = [p.def_ for p in property_stubs]
    property_rcbs = [p.resolution_callback for p in property_stubs]

    concrete_type._create_methods_and_properties(
        property_defs, property_rcbs, method_defs, method_rcbs, method_defaults
    )

