from typing import Any

def compiled_fsdp_test(compile_compute_on_module: type | None = None):
    def fully_shard_with_compiled_compute(*args, **kwargs):
        torch.distributed.fsdp.fully_shard(*args, **kwargs)  # type: ignore[operator]
        if compile_compute_on_module is None or isinstance(
            args[0], compile_compute_on_module
        ):
            args[0].compile()

    class FullyShardMode(Enum):
        EAGER = auto()
        COMPILED_COMPUTE = auto()

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            original_fully_shard: Any = torch.distributed.fsdp.fully_shard
            for mode in FullyShardMode:
                if mode != FullyShardMode.EAGER and not has_triton():
                    warnings.warn(
                        "Inductor on GPU needs Triton and recent GPU arch", stacklevel=2
                    )
                    continue
                # barrier to ensure thread reading the same value
                original_compile_threads = torch._inductor.config.compile_threads
                torch.distributed.barrier()

                if mode == FullyShardMode.EAGER:
                    fully_shard_patch = original_fully_shard
                elif mode == FullyShardMode.COMPILED_COMPUTE:
                    torch._inductor.config.compile_threads = 1
                    fully_shard_patch = fully_shard_with_compiled_compute  # type: ignore[assignment]
                else:
                    raise NotImplementedError(
                        f"Need to implement FullyShardMode={mode}"
                    )

                # fully_shard is imported as a global
                # through `from ... import fully_shard`
                func.__globals__[original_fully_shard.__name__] = fully_shard_patch
                func(*args, **kwargs)
                # other threads use patched func before this thread restores
                torch.distributed.barrier()
                func.__globals__[original_fully_shard.__name__] = original_fully_shard
                torch._inductor.config.compile_threads = original_compile_threads

        return wrapper

    return decorator

