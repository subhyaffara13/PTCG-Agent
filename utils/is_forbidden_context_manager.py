import sys
from typing import Any

def is_forbidden_context_manager(ctx: object) -> bool:
    f_ctxs: list[Any] = []

    try:
        from _pytest.python_api import RaisesContext  # type: ignore[attr-defined]
        from _pytest.recwarn import WarningsChecker  # type: ignore[attr-defined]

        f_ctxs.append(RaisesContext)
        f_ctxs.append(WarningsChecker)
    except ImportError:
        pass

    if m := sys.modules.get("torch.testing._internal.jit_utils"):
        f_ctxs.append(m._AssertRaisesRegexWithHighlightContext)

    return ctx in f_ctxs

