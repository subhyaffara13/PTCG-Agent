
def _check_rng_sync_internal(
    generator: torch.Generator, group: dist.ProcessGroup
) -> tuple[dict[Any, set], str]:
    if generator.device.type == "cuda":
        return _check_philox_rng_sync(generator, group)
    elif generator.device.type == "cpu":
        return _check_cpu_rng_sync(generator, group)
    else:
        raise NotImplementedError(
            f"Unsupported generator device: {generator.device.type}"
        )

