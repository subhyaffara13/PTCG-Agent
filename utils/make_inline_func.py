from typing import Callable

def make_inline_func(rule: RuleDictType) -> Callable[[StateInline, bool], bool]:
    def _func(state: StateInline, silent: bool) -> bool:
        res = applyRule(rule, state.src, state.pos, False)
        if res:
            if not silent:
                token = state.push(rule["name"], "math", 0)
                token.content = res[1]  # group 1 from regex ..
                token.markup = rule["tag"]

            state.pos += res.end()

        return bool(res)

    return _func

