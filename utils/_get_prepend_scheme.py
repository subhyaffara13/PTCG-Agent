
def _get_prepend_scheme(add_prefix_space: bool, original_tokenizer) -> str:
    if add_prefix_space:
        prepend_scheme = "always"
        if not getattr(original_tokenizer, "legacy", True):
            prepend_scheme = "first"
    else:
        prepend_scheme = "never"
    return prepend_scheme


def _get_prepend_scheme(add_prefix_space: bool, original_tokenizer) -> str:
    if add_prefix_space:
        prepend_scheme = "always"
        if not getattr(original_tokenizer, "legacy", True):
            prepend_scheme = "first"
    else:
        prepend_scheme = "never"
    return prepend_scheme

