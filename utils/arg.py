import re
from typing import Any
import math


def Arg(type=Any, name=None):
    """A normal positional argument"""
    return type


def arg(x):
    if type(x) is float:
        return math.atan2(0.0,x)
    return math.atan2(x.imag,x.real)


def arg(ctx, x):
    x = ctx.convert(x)
    re = ctx._re(x)
    im = ctx._im(x)
    return ctx.atan2(im, re)

