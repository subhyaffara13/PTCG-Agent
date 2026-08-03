import sys
from typing import Any

def with_comms(
    eager_init: TestFunc | bool = False,
    backend: str | None = None,
) -> TestFunc:
    def decorator(func, eager_init: bool = False, backend: str | None = None):
        @wraps(func)  # pyre-ignore[6]
        def wrapper(
            self,
            *args: tuple[object],
            **kwargs: dict[str, Any],  # type: ignore[misc]
        ) -> None:
            # just passthrough if harness doesn't
            # support init_pg e.g., DTensorOpTestBase
            if not hasattr(self, "init_pg"):
                func(self, *args, **kwargs)
                return

            self.init_pg(eager_init, backend)

            try:
                func(self, *args, **kwargs)  # type: ignore[misc]
            except Exception as e:
                dist.destroy_process_group()
                raise e

            self.destroy_pg()

        return wrapper

    return (
        decorator(func=eager_init)
        if callable(eager_init)
        else partial(decorator, eager_init=eager_init, backend=backend)
    )


def with_comms(func=None, init_rpc=True, backend="nccl"):
    if func is None:
        return partial(
            with_comms,
            init_rpc=init_rpc,
            backend=backend,
        )

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if backend == "nccl" and torch.cuda.device_count() < self.world_size:
            sys.exit(TEST_SKIPS[f"multi-gpu-{self.world_size}"].exit_code)
        self.init_comms(init_rpc=init_rpc, backend=backend)
        func(self, *args, **kwargs)
        self.destroy_comms(destroy_rpc=init_rpc)

    return wrapper

