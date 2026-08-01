
def _typing_transform():
    code = textwrap.dedent(
        """
    class Generic:
        @classmethod
        def __class_getitem__(cls, item):  return cls
    class ParamSpec:
        @property
        def args(self):
            return ParamSpecArgs(self)
        @property
        def kwargs(self):
            return ParamSpecKwargs(self)
    class ParamSpecArgs: ...
    class ParamSpecKwargs: ...
    class TypeAlias: ...
    class Type:
        @classmethod
        def __class_getitem__(cls, item):  return cls
    class TypeVar:
        @classmethod
        def __class_getitem__(cls, item):  return cls
    class TypeVarTuple: ...
    class ContextManager:
        @classmethod
        def __class_getitem__(cls, item):  return cls
    class AsyncContextManager:
        @classmethod
        def __class_getitem__(cls, item):  return cls
    class Pattern:
        @classmethod
        def __class_getitem__(cls, item):  return cls
    class Match:
        @classmethod
        def __class_getitem__(cls, item):  return cls
    """
    )
    if PY314_PLUS:
        code += textwrap.dedent(
            """
    from annotationlib import ForwardRef
    class Union:
        @classmethod
        def __class_getitem__(cls, item): return cls
    """
        )
    return AstroidBuilder(AstroidManager()).string_build(code)

