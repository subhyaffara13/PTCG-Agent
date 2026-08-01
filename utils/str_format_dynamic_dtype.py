
def str_format_dynamic_dtype(op):
    fmt_str = f"""
        OpInfo({op.name},
               dtypes={dtypes_dispatch_hint(op.dtypes).dispatch_fn_str},
               dtypesIfCUDA={dtypes_dispatch_hint(op.dtypesIfCUDA).dispatch_fn_str},
        )
        """

    return fmt_str

