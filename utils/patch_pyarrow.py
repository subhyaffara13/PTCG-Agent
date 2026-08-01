
def patch_pyarrow() -> None:
    # starting from pyarrow 14.0.1, it has its own mechanism
    if not pa_version_under14p1:
        return

    # if https://github.com/pitrou/pyarrow-hotfix was installed and enabled
    if getattr(pyarrow, "_hotfix_installed", False):
        return

    class ForbiddenExtensionType(pyarrow.ExtensionType):
        def __arrow_ext_serialize__(self) -> bytes:
            return b""

        @classmethod
        def __arrow_ext_deserialize__(cls, storage_type, serialized):
            import io
            import pickletools

            out = io.StringIO()
            pickletools.dis(serialized, out)
            raise RuntimeError(
                _ERROR_MSG.format(
                    storage_type=storage_type,
                    serialized=serialized,
                    pickle_disassembly=out.getvalue(),
                )
            )

    pyarrow.unregister_extension_type("arrow.py_extension_type")
    pyarrow.register_extension_type(
        ForbiddenExtensionType(pyarrow.null(), "arrow.py_extension_type")
    )

    pyarrow._hotfix_installed = True

