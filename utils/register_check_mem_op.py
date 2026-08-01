
def register_check_mem_op() -> None:
    lib = torch.library.Library("_inductor_debug", "FRAGMENT")  # noqa: TOR901
    lib.define(
        "check_memory_step(str[] allocated, str[] freed, bool is_final_step) -> ()"
    )
    lib.impl("check_memory_step", check_memory_step, "BackendSelect")
    from torch._higher_order_ops.effects import _EffectType, _register_effectful_op

    _register_effectful_op(
        torch.ops._inductor_debug.check_memory_step.default,
        _EffectType.ORDERED,
    )

