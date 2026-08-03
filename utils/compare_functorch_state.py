from typing import Any

def compare_functorch_state(states: list[tuple[Any, ...]]) -> bool:
    # There are four possible cases covered here:
    # 1. Current stack empty AND stack when generated not empty -> Invalidate
    # 2. Current stack not empty AND stack when generated empty -> Invalidate
    # 3. Current stack and generated stack empty -> Valid FX graph
    # 4. Current stack and generated stack not empty -> Valid if both states match
    peek = torch._C._functorch.peek_interpreter_stack()
    if (peek is None and len(states) != 0) or (peek is not None and len(states) == 0):
        return False

    cis = retrieve_all_functorch_interpreters()
    return len(cis) == len(states) and all(
        ci.check_state(state) for ci, state in zip(cis, states)
    )

