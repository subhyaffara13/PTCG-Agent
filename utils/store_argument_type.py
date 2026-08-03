from typing import Callable

def store_argument_type(
    defn: FuncItem, i: int, typ: CallableType, named_type: Callable[[str, list[Type]], Instance]
) -> None:
    arg_type = typ.arg_types[i]
    if typ.arg_kinds[i] == ARG_STAR:
        if isinstance(arg_type, ParamSpecType):
            pass
        elif isinstance(arg_type, UnpackType):
            unpacked_type = get_proper_type(arg_type.type)
            if isinstance(unpacked_type, TupleType):
                # Instead of using Tuple[Unpack[Tuple[...]]], just use Tuple[...]
                arg_type = unpacked_type
            elif (
                isinstance(unpacked_type, Instance)
                and unpacked_type.type.fullname == "builtins.tuple"
            ):
                arg_type = unpacked_type
            else:
                # TODO: verify that we can only have a TypeVarTuple here.
                arg_type = TupleType(
                    [arg_type],
                    fallback=named_type("builtins.tuple", [named_type("builtins.object", [])]),
                )
        else:
            # builtins.tuple[T] is typing.Tuple[T, ...]
            arg_type = named_type("builtins.tuple", [arg_type])
    elif typ.arg_kinds[i] == ARG_STAR2:
        if not isinstance(arg_type, ParamSpecType) and not typ.unpack_kwargs:
            arg_type = named_type("builtins.dict", [named_type("builtins.str", []), arg_type])
    defn.arguments[i].variable.type = arg_type

