
def gen_registration_helpers(backend_index: BackendIndex) -> list[str]:
    return [
        'C10_DIAGNOSTIC_PUSH_AND_IGNORED_IF_DEFINED("-Wunused-function")',
        *gen_create_out_helper(backend_index),
        *gen_resize_out_helper(backend_index),
        *gen_check_inplace_helper(backend_index),
        *gen_maybe_create_proxy_helper(backend_index),
        "C10_DIAGNOSTIC_POP()",
    ]

