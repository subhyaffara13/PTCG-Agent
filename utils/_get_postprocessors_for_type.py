
def _get_postprocessors_for_type(arg_type):
    return tuple(
        Basic._constructor_postprocessor_mapping[cls]
        for cls in arg_type.mro()
        if cls in Basic._constructor_postprocessor_mapping
    )

