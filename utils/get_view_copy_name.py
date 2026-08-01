
def get_view_copy_name(f: NativeFunction) -> OperatorName:
    # Right now, when asking for a view op's corresponding "view_copy" name
    # we assert for sanity that the op is allowed to have a generated view_copy variant.
    # (We can do this because "gets_generated_view_copy()" tell us which ops get a generated view_copy op).
    # However, narrow_copy() already exists as an op directly in native_functions.yaml.
    # I'm hardcoding narrow_copy here for now to maintain the assert,
    # But we could also just get rid of the assert.
    list_of_ops_with_explicit_view_copy_operators = ["narrow"]
    if str(f.func.name) not in list_of_ops_with_explicit_view_copy_operators:
        if not gets_generated_view_copy(f):
            raise AssertionError(
                f"{f.func.name} does not have a generated view_copy variant"
            )

    base_name = f"{f.func.name.name.base}_copy"
    view_copy_name = OperatorName(
        name=BaseOperatorName(
            base=base_name, inplace=False, dunder_method=f.func.name.name.dunder_method
        ),
        overload_name=f.func.name.overload_name,
    )
    return view_copy_name

