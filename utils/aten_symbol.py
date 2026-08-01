
def aten_symbol(schema: LazyIrSchema) -> str:
    missing_interned_strings = {
        "sigmoid_backward",
    }
    if schema.aten_name in missing_interned_strings:
        return f'c10::Symbol::fromQualString("aten::{schema.aten_name}")'

    if not schema.aten_name.startswith("at::"):
        return f"at::aten::{schema.aten_name}"
    else:
        return schema.aten_name

