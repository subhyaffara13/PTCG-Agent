
def _run_function(python_udf):
    r"""
    This function is exclusively called from C++.
    See ``torch/csrc/distributed/rpc/python_rpc_handler.cpp``.

    Runs a Python UDF and returns its return value.
    Wraps any exception in ``RemoteException`` if the function raises.
    """
    try:
        if isinstance(python_udf, AttributeError):
            raise python_udf
        result = python_udf.func(*python_udf.args, **python_udf.kwargs)
    except Exception as e:
        # except str = exception info + traceback string
        except_str = (
            f"On {_get_current_rpc_agent().get_worker_info()}:\n"
            f"{repr(e)}\n{traceback.format_exc()}"
        )
        print(except_str, file=sys.stderr)
        result = RemoteException(except_str, type(e))
    return result

