
def test_module(module_name: str) -> Iterator[Error]:
    """Tests a given module's stub against introspecting it at runtime.

    Requires the stub to have been built already, accomplished by a call to ``build_stubs``.

    :param module_name: The module to test

    """
    stub = get_stub(module_name)
    if stub is None:
        if not is_probably_private(module_name.split(".")[-1]):
            runtime_desc = repr(sys.modules[module_name]) if module_name in sys.modules else "N/A"
            yield Error(
                [module_name], "failed to find stubs", MISSING, None, runtime_desc=runtime_desc
            )
        return

    try:
        runtime = silent_import_module(module_name)
    except KeyboardInterrupt:
        raise
    except BaseException as e:
        note = ""
        if isinstance(e, ModuleNotFoundError):
            note = " Maybe install the runtime package or alter PYTHONPATH?"
        yield Error(
            [module_name], f"failed to import.{note} {type(e).__name__}: {e}", stub, MISSING
        )
        return

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            yield from verify(stub, runtime, [module_name])
        except Exception as e:
            bottom_frame = list(traceback.walk_tb(e.__traceback__))[-1][0]
            bottom_module = bottom_frame.f_globals.get("__name__", "")
            # Pass on any errors originating from stubtest or mypy
            # These can occur expectedly, e.g. StubtestFailure
            if bottom_module == "__main__" or bottom_module.split(".")[0] == "mypy":
                raise
            yield Error(
                [module_name],
                f"encountered unexpected error, {type(e).__name__}: {e}",
                stub,
                runtime,
                stub_desc="N/A",
                runtime_desc=(
                    "This is most likely the fault of something very dynamic in your library. "
                    "It's also possible this is a bug in stubtest.\nIf in doubt, please "
                    "open an issue at https://github.com/python/mypy\n\n"
                    + traceback.format_exc().strip()
                ),
            )

