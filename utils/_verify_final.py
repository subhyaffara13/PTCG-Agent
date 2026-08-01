
def _verify_final(
    stub: nodes.TypeInfo, runtime: type[Any], object_path: list[str]
) -> Iterator[Error]:
    try:

        class SubClass(runtime):  # type: ignore[misc]
            pass

    except TypeError:
        # Enum classes are implicitly @final
        if not stub.is_final and not issubclass(runtime, enum.Enum):
            yield Error(
                object_path,
                "cannot be subclassed at runtime, but isn't marked with @final in the stub",
                stub,
                runtime,
                stub_desc=repr(stub),
            )
    except Exception:
        # The class probably wants its subclasses to do something special.
        # Examples: ctypes.Array, ctypes._SimpleCData
        pass

    # Runtime class might be annotated with `@final`:
    try:
        runtime_final = getattr(runtime, "__final__", False)
    except Exception:
        runtime_final = False

    if runtime_final and not stub.is_final:
        yield Error(
            object_path,
            "has `__final__` attribute, but isn't marked with @final in the stub",
            stub,
            runtime,
            stub_desc=repr(stub),
        )

