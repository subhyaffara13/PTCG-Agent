
def check_native_override(
    builder: IRBuilder, base_sig: FuncSignature, sub_sig: FuncSignature, line: int
) -> None:
    """Report an error if an override changes signature in unsupported ways.

    Glue methods can work around many signature changes but not all of them.
    """
    for base_arg, sub_arg in zip(base_sig.real_args(), sub_sig.real_args()):
        if base_arg.type.error_overlap:
            if not base_arg.optional and sub_arg.optional and base_sig.num_bitmap_args:
                # This would change the meanings of bits in the argument defaults
                # bitmap, which we don't support. We'd need to do tricky bit
                # manipulations to support this generally.
                builder.error(
                    "An argument with type "
                    + f'"{base_arg.type}" cannot be given a default value in a method override',
                    line,
                )
        if base_arg.type.error_overlap or sub_arg.type.error_overlap:
            if not is_same_type(base_arg.type, sub_arg.type):
                # This would change from signaling a default via an error value to
                # signaling a default via bitmap, which we don't support.
                builder.error(
                    "Incompatible argument type "
                    + f'"{sub_arg.type}" (base class has type "{base_arg.type}")',
                    line,
                )

