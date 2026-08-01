
def op_name_from_native_function(f: NativeFunction) -> str:
    # This was originally read from the 'operator_name_with_overload' field in the
    # declaration dict, which was the part before the first '(' in 'schema_string'.
    return f"{f.namespace}::{f.func.name}"

