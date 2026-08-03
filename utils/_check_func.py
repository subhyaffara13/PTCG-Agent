from typing import Any, Callable

def _check_func(checker, argname, thefunc, x0, args, numinputs,
                output_shape=None):
    res = atleast_1d(thefunc(*((x0[:numinputs],) + args)))
    if (output_shape is not None) and (shape(res) != output_shape):
        if (output_shape[0] != 1):
            if len(output_shape) > 1:
                if output_shape[1] == 1:
                    return shape(res)
            msg = f"{checker}: there is a mismatch between the input and output " \
                  f"shape of the '{argname}' argument"
            func_name = getattr(thefunc, '__name__', None)
            if func_name:
                msg += f" '{func_name}'."
            else:
                msg += "."
            msg += f' Shape should be {output_shape} but it is {shape(res)}.'
            raise TypeError(msg)
    if issubdtype(res.dtype, inexact):
        dt = res.dtype
    else:
        dt = dtype(float)
    return shape(res), dt


def _check_func(
    func: Callable[[Any], bool], predicate_err: str | Callable[[], str], s: cs.CoreSchema | None
) -> cs.CoreSchema:
    def handler(v: Any) -> Any:
        if func(v):
            return v
        raise ValueError(f'Expected {predicate_err if isinstance(predicate_err, str) else predicate_err()}')

    if s is None:
        return cs.no_info_plain_validator_function(handler)
    else:
        return cs.no_info_after_validator_function(handler, s)

