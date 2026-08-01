
def _check_pystubs_once(func, qualname, actual_module_name):
    checked = False

    def inner(*args, **kwargs):
        nonlocal checked
        if checked:
            return func(*args, **kwargs)

        op = torch._library.utils.lookup_op(qualname)
        if op._defined_in_python:
            checked = True
            return func(*args, **kwargs)

        maybe_pystub = torch._C._dispatch_pystub(
            op._schema.name, op._schema.overload_name
        )
        if maybe_pystub is None:
            if torch._library.utils.requires_set_python_module():
                namespace = op.namespace
                cpp_filename = op._handle.debug()
                raise RuntimeError(
                    f"Operator '{qualname}' was defined in C++ and has a Python "
                    f"fake impl. In this situation, we require there to also be a "
                    f'companion C++ `m.set_python_module("{actual_module_name}")` '
                    f"call, but we could not find one. Please add that to "
                    f"to the top of the C++ TORCH_LIBRARY({namespace}, ...) block the "
                    f"operator was registered in ({cpp_filename})"
                )
        else:
            pystub_module = maybe_pystub[0]
            if actual_module_name != pystub_module:
                cpp_filename = op._handle.debug()
                raise RuntimeError(
                    f"Operator '{qualname}' specified that its python fake impl "
                    f"is in the Python module '{pystub_module}' but it was actually found "
                    f"in '{actual_module_name}'. Please either move the fake impl "
                    f"or correct the m.set_python_module call ({cpp_filename})"
                )
        checked = True
        return func(*args, **kwargs)

    return inner

