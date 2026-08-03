from typing import Callable

def check_arg_kinds(
    arg_kinds: list[ArgKind], nodes: list[T], fail: Callable[[str, T], None]
) -> None:
    is_var_arg = False
    is_kw_arg = False
    seen_named = False
    seen_opt = False
    for kind, node in zip(arg_kinds, nodes):
        if kind == ARG_POS:
            if is_var_arg or is_kw_arg or seen_named or seen_opt:
                fail(
                    "Required positional args may not appear after default, named or var args",
                    node,
                )
                break
        elif kind == ARG_OPT:
            if is_var_arg or is_kw_arg or seen_named:
                fail("Positional default args may not appear after named or var args", node)
                break
            seen_opt = True
        elif kind == ARG_STAR:
            if is_var_arg or is_kw_arg or seen_named:
                fail("Var args may not appear after named or var args", node)
                break
            is_var_arg = True
        elif kind == ARG_NAMED or kind == ARG_NAMED_OPT:
            seen_named = True
            if is_kw_arg:
                fail("A **kwargs argument must be the last argument", node)
                break
        elif kind == ARG_STAR2:
            if is_kw_arg:
                fail("You may only have one **kwargs argument", node)
                break
            is_kw_arg = True

