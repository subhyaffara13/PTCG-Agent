
def is_pydantic_available() -> bool:
    return _is_package_available("pydantic")[0]


def is_pydantic_available() -> bool:
    if not is_package_available("pydantic"):
        return False
    # For Pydantic, we add an extra check to test whether it is correctly installed or not. If both pydantic 2.x and
    # typing_extensions<=4.5.0 are installed, then pydantic will fail at import time. This should not happen when
    # it is installed with `pip install huggingface_hub[inference]` but it can happen when it is installed manually
    # by the user in an environment that we don't control.
    #
    # Usually we won't need to do this kind of check on optional dependencies. However, pydantic is a special case
    # as it is automatically imported when doing `from huggingface_hub import ...` even if the user doesn't use it.
    #
    # See https://github.com/huggingface/huggingface_hub/pull/1829 for more details.
    try:
        from pydantic import validator  # noqa: F401
    except ImportError:
        # Example: "ImportError: cannot import name 'TypeAliasType' from 'typing_extensions'"
        warnings.warn(
            "Pydantic is installed but cannot be imported. Please check your installation. `huggingface_hub` will "
            "default to not using Pydantic. Error message: '{e}'"
        )
        return False
    return True

