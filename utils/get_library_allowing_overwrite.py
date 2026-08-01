
def get_library_allowing_overwrite(
    namespace: str, name: str
) -> "torch.library.Library":
    qualname = f"{namespace}::{name}"

    if qualname in OPDEF_TO_LIB:
        OPDEF_TO_LIB[qualname]._destroy()
        del OPDEF_TO_LIB[qualname]

    lib = torch.library.Library(namespace, "FRAGMENT")  # noqa: TOR901
    OPDEF_TO_LIB[qualname] = lib
    return lib

