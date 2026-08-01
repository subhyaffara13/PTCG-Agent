
def validate_hf_hub_args(fn: CallableT) -> CallableT:
    """Validate values received as argument for any public method of `huggingface_hub`.

    The goal of this decorator is to harmonize validation of arguments reused
    everywhere. By default, all defined validators are tested.

    Validators:
        - [`~utils.validate_repo_id`]: `repo_id` must be `"repo_name"`
          or `"namespace/repo_name"`. Namespace is a username or an organization.
        - [`~utils.smoothly_deprecate_legacy_arguments`]: Ignore `proxies` when downloading files (should be set globally).

    Example:
    ```py
    >>> from huggingface_hub.utils import validate_hf_hub_args

    >>> @validate_hf_hub_args
    ... def my_cool_method(repo_id: str):
    ...     print(repo_id)

    >>> my_cool_method(repo_id="valid_repo_id")
    valid_repo_id

    >>> my_cool_method("other..repo..id")
    huggingface_hub.utils._validators.HFValidationError: Cannot have -- or .. in repo_id: 'other..repo..id'.

    >>> my_cool_method(repo_id="other..repo..id")
    huggingface_hub.utils._validators.HFValidationError: Cannot have -- or .. in repo_id: 'other..repo..id'.
    ```

    Raises:
        [`~utils.HFValidationError`]:
            If an input is not valid.
    """
    # TODO: add an argument to opt-out validation for specific argument?
    signature = inspect.signature(fn)

    @wraps(fn)
    def _inner_fn(*args, **kwargs):
        for arg_name, arg_value in chain(
            zip(signature.parameters, args),  # Args values
            kwargs.items(),  # Kwargs values
        ):
            if arg_name in ["repo_id", "from_id", "to_id"]:
                validate_repo_id(arg_value)

        kwargs = smoothly_deprecate_legacy_arguments(fn_name=fn.__name__, kwargs=kwargs)

        return fn(*args, **kwargs)

    return _inner_fn  # type: ignore

