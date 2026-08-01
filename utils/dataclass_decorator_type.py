
def dataclass_decorator_type(d: Expression) -> str | None:
    if isinstance(d, RefExpr) and d.fullname in DATACLASS_DECORATORS:
        return d.fullname.split(".")[0]
    elif (
        isinstance(d, CallExpr)
        and isinstance(d.callee, RefExpr)
        and d.callee.fullname in DATACLASS_DECORATORS
    ):
        name = d.callee.fullname.split(".")[0]
        if name == "attr" and "auto_attribs" in d.arg_names:
            # Note: the mypy attrs plugin checks that the value of auto_attribs is
            # not computed at runtime, so we don't need to perform that check here
            auto = d.args[d.arg_names.index("auto_attribs")]
            if isinstance(auto, NameExpr) and auto.name == "True":
                return "attr-auto"
        return name
    else:
        return None

