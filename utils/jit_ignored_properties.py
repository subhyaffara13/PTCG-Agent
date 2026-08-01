
def jit_ignored_properties(module):
    user_annotated_ignored_attributes = getattr(
        module, "__jit_ignored_attributes__", []
    )

    def get_properties_names(module):
        return {k for k, v in vars(module).items() if isinstance(v, property)}

    properties = get_properties_names(type(module))
    user_annoted_ignored_properties = set()

    for ignored_attr in user_annotated_ignored_attributes:
        if ignored_attr in properties:
            user_annoted_ignored_properties.add(ignored_attr)
    return user_annoted_ignored_properties

