
def _get_global_builtins():
    # Taken from the 'globals' map in torch/csrc/jit/frontend/ir_emitter.cpp
    supported_builtins = [
        "print",
        "tuple",
        "float",
        "complex",
        "int",
        "bool",
        "str",
        "getattr",
        "hasattr",
        "isinstance",
        "len",
        "hex",
        "oct",
        "round",
        "hash",
        "min",
        "max",
        "abs",
        "all",
        "divmod",
        "list",
        "ord",
        "chr",
        "bin",
        "range",
        "zip",
        "enumerate",
        "sorted",
    ]

    op_renames = {
        "bool": "aten::Bool",
        "int": "aten::Int",
        "float": "aten::Float",
        "complex": "aten::Complex",
        "abs": "prim::abs",
        "max": "prim::max",
        "min": "prim::min",
        "range": "fake::does_not_exist",
    }

    schemaless_op_explanations = {
        "print": "Print any value",
        "tuple": "Lists cannot be converted to tuples with this method since their size is not statically known",
        "getattr": "Attribute name must be a literal string",
        "hasattr": "Attribute name must be a literal string",
        "isinstance": "Result is static",
        "zip": "Arguments must be iterable.",
        "enumerate": "Arguments must be iterable.",
        "range": "Can only be used as an iterator in a for loop",
    }

    magic_methods = [
        ("complex", "__complex__"),
        ("float", "__float__"),
        ("int", "__int__"),
        ("bool", "__bool__"),
        ("str", "__str__"),
        ("len", "__len__"),
        ("hex", "__hex__"),
        ("oct", "__oct__"),
    ]

    magic_methods_rows = []
    for fn, magic_method in magic_methods:
        # pyrefly: ignore [bad-argument-type]
        magic_methods_rows.append(f'"{fn}", "``{magic_method}``"')

    schematized_ops = []
    schemaless_ops = []

    for fn in supported_builtins:
        op_name = f"aten::{fn}"
        if fn in op_renames:
            op_name = op_renames[fn]
        schemas = torch._C._jit_get_schemas_for_operator(op_name)
        for s in schemas:
            schematized_ops.append(_emit_schema(None, fn, s, padding=0))
        if len(schemas) > 0:
            schematized_ops.append("")
        else:
            table_row = (
                f'":external+python:py:obj:`{fn}`", "{schemaless_op_explanations[fn]}"'
            )
            # pyrefly: ignore [bad-argument-type]
            schemaless_ops.append(table_row)

    schematized_ops_str = "\n".join(schematized_ops)
    schemaless_ops_str = "\n".join(schemaless_ops)
    magic_methods_rows_str = "\n".join(magic_methods_rows)
    schematized_ops_str = textwrap.indent(schematized_ops_str, "\t")
    schemaless_ops_str = textwrap.indent(schemaless_ops_str, "\t")
    magic_methods_rows_str = textwrap.indent(magic_methods_rows_str, "\t")
    section = f"""
The functions in the following table are supported but do not have a static schema

.. csv-table::
    :header: "Function", "Note"

{schemaless_ops_str}

The following functions will use the corresponding magic method on TorchScript classes

.. csv-table::
    :header: "Function", "Magic Method"

{magic_methods_rows_str}

These built-in functions use the schema

.. rst-class:: codeblock-height-limiter

::

{schematized_ops_str}
    """

    return "Python Built-in Functions", section

