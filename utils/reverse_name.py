
def reverse_name(f: NativeFunction, include_namespace: bool) -> str:
    # for the reverse: we plumb the "reapply_views" flag into that function and support
    # both copy and non-copy variants. (We could avoid doing that, but that would require
    # writing out twice as many view inverse functions).
    api_name = f.func.name.unambiguous_name()
    # in the reverse case, we codegen both the call-sites (which need the full namespace) and the declarations (which don't)
    if include_namespace:
        return f"at::functionalization::FunctionalInverses::{api_name}_inverse"
    else:
        return f"{api_name}_inverse"

