
def safe_inspect_signature(runtime: Any) -> inspect.Signature | None:
    if (
        hasattr(runtime, "__name__")
        and runtime.__name__ == "__init__"
        and hasattr(runtime, "__text_signature__")
        and runtime.__text_signature__ == "($self, /, *args, **kwargs)"
        and hasattr(runtime, "__objclass__")
        and hasattr(runtime.__objclass__, "__text_signature__")
        and runtime.__objclass__.__text_signature__ is not None
    ):
        # This is an __init__ method with the generic C-class signature.
        # In this case, the underlying class often has a better signature,
        # which we can convert into an __init__ signature by adding in the
        # self parameter.
        try:
            s = inspect.signature(runtime.__objclass__)

            parameter_kind: inspect._ParameterKind = inspect.Parameter.POSITIONAL_OR_KEYWORD
            if s.parameters:
                first_parameter = next(iter(s.parameters.values()))
                if first_parameter.kind == inspect.Parameter.POSITIONAL_ONLY:
                    parameter_kind = inspect.Parameter.POSITIONAL_ONLY
            return s.replace(
                parameters=[inspect.Parameter("self", parameter_kind), *s.parameters.values()]
            )
        except Exception:
            pass

    if (
        hasattr(runtime, "__name__")
        and runtime.__name__ == "__new__"
        and hasattr(runtime, "__text_signature__")
        and runtime.__text_signature__ == "($type, *args, **kwargs)"
        and hasattr(runtime, "__self__")
        and hasattr(runtime.__self__, "__text_signature__")
        and runtime.__self__.__text_signature__ is not None
    ):
        # This is a __new__ method with the generic C-class signature.
        # In this case, the underlying class often has a better signature,
        # which we can convert into a __new__ signature by adding in the
        # cls parameter.

        # If the attached class has a valid __init__, skip recovering a
        # signature for this __new__ method.
        has_init = False
        if (
            hasattr(runtime.__self__, "__init__")
            and hasattr(runtime.__self__.__init__, "__objclass__")
            and runtime.__self__.__init__.__objclass__ is runtime.__self__
        ):
            has_init = True

        if not has_init:
            try:
                s = inspect.signature(runtime.__self__)
                parameter_kind = inspect.Parameter.POSITIONAL_OR_KEYWORD
                if s.parameters:
                    first_parameter = next(iter(s.parameters.values()))
                    if first_parameter.kind == inspect.Parameter.POSITIONAL_ONLY:
                        parameter_kind = inspect.Parameter.POSITIONAL_ONLY
                return s.replace(
                    parameters=[inspect.Parameter("cls", parameter_kind), *s.parameters.values()]
                )
            except Exception:
                pass

    try:
        try:
            return inspect.signature(runtime)
        except ValueError:
            if (
                hasattr(runtime, "__text_signature__")
                and "<unrepresentable>" in runtime.__text_signature__
            ):
                # Try to fix up the signature. Workaround for
                # https://github.com/python/cpython/issues/87233
                sig = runtime.__text_signature__.replace("<unrepresentable>", "...")
                sig = inspect._signature_fromstr(inspect.Signature, runtime, sig)  # type: ignore[attr-defined]
                assert isinstance(sig, inspect.Signature)
                new_params = [
                    (
                        parameter.replace(default=UNREPRESENTABLE)
                        if parameter.default is ...
                        else parameter
                    )
                    for parameter in sig.parameters.values()
                ]
                return sig.replace(parameters=new_params)
            else:
                raise
    except Exception:
        # inspect.signature throws ValueError all the time
        # catch RuntimeError because of https://bugs.python.org/issue39504
        # catch TypeError because of https://github.com/python/typeshed/pull/5762
        # catch AttributeError because of inspect.signature(_curses.window.border)
        return None

