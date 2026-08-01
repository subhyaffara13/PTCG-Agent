
def inverse_view_name(f: NativeFunction) -> str:
    copy_variant = f"{f.root_name}_copy"
    overload = f"{f.func.name.overload_name}"
    if overload != "":
        overload = "_" + overload
    return f"{copy_variant}{overload}_inverse"

