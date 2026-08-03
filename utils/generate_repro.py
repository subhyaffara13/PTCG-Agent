import os
from typing import Any

def generate_repro(
    test: str,
    op: torch._ops.OpOverload,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    *,
    save_data: bool,
    dry_run: bool = False,
) -> str:
    if save_data:
        now = datetime.datetime.now()
        path = os.path.join(tempfile.gettempdir(), "pytorch_opcheck_safe_to_delete")
        unix_timestamp = datetime.datetime.timestamp(now) * 100000
        filepath = os.path.join(path, f"repro_{unix_timestamp}.pt")
        if not dry_run:
            os.makedirs(path, exist_ok=True)
            torch.save((args, kwargs), filepath)
        args_kwargs = f'args, kwargs = torch.load("{filepath}")'
    else:
        args_kwargs = (
            "# If you rerun your test with PYTORCH_OPCHECK_PRINT_BETTER_REPRO=1\n"
            "# we will fill them in same (args, kwargs) as in your test\n"
            "args = ()  # args to the operator\n"
            "kwargs = {}  # kwargs to the operator"
        )

    ns, name = op._schema.name.split("::")
    overload = op._overloadname

    repro_command = (
        f"# =========================================================\n"
        f"# BEGIN REPRO SCRIPT\n"
        f"# =========================================================\n"
        f"import torch\n"
        f"from torch.testing._internal.optests import opcheck\n"
        f"\n"
        f"# Make sure you have loaded the library that contains the op\n"
        f"# via an import or torch.ops.load_library(...)\n"
        f"op = torch.ops.{ns}.{name}.{overload}\n"
        f"\n"
        f"{args_kwargs}\n"
        f'opcheck(op, args, kwargs, test_utils="{test}")\n'
        f"# =========================================================\n"
        f"# END REPRO SCRIPT\n"
        f"# =========================================================\n"
    )
    return repro_command

