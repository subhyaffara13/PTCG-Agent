from typing import Any

def cache_real_value_when_export(
    tx: "InstructionTranslatorBase", proxy: Any, example_value: Any
) -> None:
    if tx.export:
        # The legacy behavior for real value cache with subclasses was
        # to perform a clone WITHOUT preserving the subclass.  It's
        # not entirely clear this is what you actually want though.
        with torch._C.DisableTorchFunctionSubclass():
            proxy.tracer.real_value_cache[proxy.node] = _clone_input(
                example_value, tx.fake_mode
            )

