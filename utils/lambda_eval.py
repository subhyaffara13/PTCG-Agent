from typing import Any, Callable

def lambda_eval(expression: Callable[[dict[str, Any]], Any], **kw: Any) -> Any:
    """
    Returns the result of an image function.

    :py:mod:`~PIL.ImageMath` only supports single-layer images. To process multi-band
    images, use the :py:meth:`~PIL.Image.Image.split` method or
    :py:func:`~PIL.Image.merge` function.

    :param expression: A function that receives a dictionary.
    :param **kw: Values to add to the function's dictionary.
    :return: The expression result. This is usually an image object, but can
             also be an integer, a floating point value, or a pixel tuple,
             depending on the expression.
    """

    args: dict[str, Any] = ops.copy()
    args.update(kw)
    for k, v in args.items():
        if isinstance(v, Image.Image):
            args[k] = _Operand(v)

    out = expression(args)
    try:
        return out.im
    except AttributeError:
        return out

