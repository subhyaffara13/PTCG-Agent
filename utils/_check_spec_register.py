
def _check_spec_register(testing_spec: EnvSpec):
    """Checks whether the spec is valid to be registered. Helper function for `register`."""
    latest_versioned_spec = max(
        (
            env_spec
            for env_spec in registry.values()
            if env_spec.namespace == testing_spec.namespace
            and env_spec.name == testing_spec.name
            and env_spec.version is not None
        ),
        key=lambda spec_: int(spec_.version),  # type: ignore
        default=None,
    )

    unversioned_spec = next(
        (
            env_spec
            for env_spec in registry.values()
            if env_spec.namespace == testing_spec.namespace
            and env_spec.name == testing_spec.name
            and env_spec.version is None
        ),
        None,
    )

    if unversioned_spec is not None and testing_spec.version is not None:
        raise error.RegistrationError(
            "Can't register the versioned environment "
            f"`{testing_spec.id}` when the unversioned environment "
            f"`{unversioned_spec.id}` of the same name already exists."
        )
    elif latest_versioned_spec is not None and testing_spec.version is None:
        raise error.RegistrationError(
            f"Can't register the unversioned environment `{testing_spec.id}` when the versioned environment "
            f"`{latest_versioned_spec.id}` of the same name already exists. Note: the default behavior is "
            "that `gym.make` with the unversioned environment will return the latest versioned environment"
        )


def _check_spec_register(spec: EnvSpec):
    """Checks whether the spec is valid to be registered. Helper function for `register`."""
    global registry
    latest_versioned_spec = max(
        (
            spec_
            for spec_ in registry.values()
            if spec_.namespace == spec.namespace
            and spec_.name == spec.name
            and spec_.version is not None
        ),
        key=lambda spec_: int(spec_.version),  # type: ignore
        default=None,
    )

    unversioned_spec = next(
        (
            spec_
            for spec_ in registry.values()
            if spec_.namespace == spec.namespace
            and spec_.name == spec.name
            and spec_.version is None
        ),
        None,
    )

    if unversioned_spec is not None and spec.version is not None:
        raise error.RegistrationError(
            "Can't register the versioned environment "
            f"`{spec.id}` when the unversioned environment "
            f"`{unversioned_spec.id}` of the same name already exists."
        )
    elif latest_versioned_spec is not None and spec.version is None:
        raise error.RegistrationError(
            "Can't register the unversioned environment "
            f"`{spec.id}` when the versioned environment "
            f"`{latest_versioned_spec.id}` of the same name "
            f"already exists. Note: the default behavior is "
            f"that `gym.make` with the unversioned environment "
            f"will return the latest versioned environment"
        )

