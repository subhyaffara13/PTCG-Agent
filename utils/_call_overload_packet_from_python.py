
def _call_overload_packet_from_python(
    op: OpOverloadPacket[_P, _T], *args: _P.args, **kwargs: _P.kwargs
) -> _T:
    # Reuse the torch function handling logic in cpp
    torch_function_called, ret = torch._C._maybe_call_torch_function_for_op_packet(
        op, *args, **kwargs
    )

    if torch_function_called:
        return ret

    # The following mirrors getOpWithStack.
    # In cpp, we do a schema matching for the arguments, and call ToIValue to
    # to check whether the arguments are valid. But need to do similar things here
    # and check the schema whether the FakeScriptObject is the corresponding fake class
    # of the actual class used in schema.
    exceptions = {}
    found_op = None
    for overload_name in op.overloads():
        op_overload = getattr(op, overload_name)
        try:
            _ = torch._C._check_schema_allow_fake_script_object(
                op_overload._schema, *args, **kwargs
            )
            found_op = op_overload
            break
        except RuntimeError as e:
            exceptions[overload_name] = e

    if found_op:
        return found_op(*args, **kwargs)

    err_msg = (
        f"Fail to match any TorchBindOverload of {op} with following exceptions:\n"
    )
    for key, msg in exceptions.items():
        err_msg += f"Overload name {key}:\n {msg}\n"
    raise RuntimeError(err_msg)

