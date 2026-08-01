
def gen_inplace_or_view_type_env(
    fn: NativeFunctionWithDifferentiabilityInfo,
) -> dict[str, list[str]]:
    definition = inplace_or_view_method_definition(fn)
    registration = inplace_or_view_method_registration(fn)

    return {
        "ops_headers": (
            [f"#include <ATen/ops/{fn.func.root_name}_ops.h>"]
            if definition is not None
            else []
        ),
        "inplace_or_view_method_definitions": [definition]
        if definition is not None
        else [],
        "inplace_or_view_wrapper_registrations": [registration]
        if registration is not None
        else [],
    }

