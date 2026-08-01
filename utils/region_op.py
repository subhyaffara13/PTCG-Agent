
def region_op(op_constructor, terminator=None):
    """Decorator to define an MLIR Op specified as a python function.

    Requires that an `mlir.ir.InsertionPoint` and `mlir.ir.Location` are
    active for the current thread (i.e. established in a `with` block).

    Supports "naked" usage i.e., no parens if no args need to be passed to the Op constructor.

    When applied as a decorator to a Python function, an entry block will
    be constructed for the Op with types as specified **as type hints on the args of the function**.
    The block arguments will be passed positionally to the Python function.

    If a terminator is specified then the return from the decorated function will be passed
    to the terminator as the last statement in the entry block. Note, the API for the terminator
    is a (possibly empty) list; terminator accepting single values should be wrapped in a
    `lambda args: term(args[0])`

    The identifier (name) of the function will become:
    1. A single value result if the Op returns a single value;
    2. An OpResultList (as a list) if the Op returns multiple values;
    3. The Operation if the Op returns no results.

    See examples in tensor.py and transform.extras.
    """

    def op_decorator(*args, **kwargs):
        op = op_constructor(*args, **kwargs)
        op_region = op.regions[0]

        return op_region_builder(op, op_region, terminator)

    @wraps(op_decorator)
    def maybe_no_args(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            return op_decorator()(args[0])
        else:
            return op_decorator(*args, **kwargs)

    return maybe_no_args

