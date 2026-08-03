import functools
import sys
from typing import Any

def repro_minifier_query(options: Any, mod: nn.Module, load_args: Any) -> None:
    mod, args = repro_common(options, mod, load_args)
    fail_fn = functools.partial(
        ACCURACY_FAILS[options.accuracy],
        check_str=options.check_str,  # type: ignore[call-arg]
    )
    if fail_fn(mod, args):
        sys.exit(1)
    else:
        sys.exit(0)

