import functools

def requires(distribution_name: str) -> list[str] | None:
    """
    Return a list of requirements for the named package.

    :return: An iterable of requirements, suitable for
        packaging.requirement.Requirement.
    """
    return distribution(distribution_name).requires


def requires(*, backends=()):
    """
    This decorator enables two things:
    - Attaching a `__backends` tuple to an object to see what are the necessary backends for it
      to execute correctly without instantiating it
    - The '@requires' string is used to dynamically import objects
    """

    if not isinstance(backends, (tuple, list)):
        raise TypeError("Backends should be a tuple or list.")
    backends = tuple(backends)

    applied_backends = []
    for backend in backends:
        if backend in BACKENDS_MAPPING:
            applied_backends.append(backend)
        else:
            if any(key in backend for key in ["=", "<", ">"]):
                applied_backends.append(Backend(backend))
            else:
                raise ValueError(f"Backend should be defined in the BACKENDS_MAPPING. Offending backend: {backend}")

    def inner_fn(fun):
        if isinstance(fun, type):
            # For classes, just attach the metadata — don't wrap, as that would
            # turn the class into a plain function and break isinstance checks.
            fun.__backends = applied_backends
            return fun

        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            requires_backends(fun, applied_backends)
            return fun(*args, **kwargs)

        wrapper.__backends = applied_backends  # type: ignore [unresolved-attribute]
        return wrapper

    return inner_fn


def requires(distribution_name: str) -> list[str] | None:
    """
    Return a list of requirements for the named package.

    :return: An iterable of requirements, suitable for
        packaging.requirement.Requirement.
    """
    return distribution(distribution_name).requires

