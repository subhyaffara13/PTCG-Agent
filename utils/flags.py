
def flags(fp32_precision="none"):
    with __allow_nonbracketed_mutation():
        orig_flags = set_flags(fp32_precision)
    try:
        yield
    finally:
        with __allow_nonbracketed_mutation():
            set_flags(*orig_flags)


def flags(
    enabled=False,
    benchmark=False,
    benchmark_limit=10,
    deterministic=False,
    allow_tf32=True,
    fp32_precision="none",
):
    with __allow_nonbracketed_mutation():
        orig_flags = set_flags(
            enabled,
            benchmark,
            benchmark_limit,
            deterministic,
            allow_tf32,
            fp32_precision,
        )
    try:
        yield
    finally:
        # recover the previous values
        with __allow_nonbracketed_mutation():
            set_flags(*orig_flags)


def flags(
    immediate=False,
):
    with __allow_nonbracketed_mutation():
        orig_flags = set_flags(
            immediate,
        )
    try:
        yield
    finally:
        # recover the previous values
        with __allow_nonbracketed_mutation():
            set_flags(*orig_flags)


def flags(enabled=False, deterministic=False, allow_tf32=True, fp32_precision="none"):
    with __allow_nonbracketed_mutation():
        orig_flags = set_flags(enabled, deterministic, allow_tf32, fp32_precision)
    try:
        yield
    finally:
        with __allow_nonbracketed_mutation():
            set_flags(*orig_flags)


def flags(enabled=False):
    r"""Context manager for setting if nnpack is enabled globally"""
    with __allow_nonbracketed_mutation():
        orig_flags = set_flags(enabled)
    try:
        yield
    finally:
        with __allow_nonbracketed_mutation():
            set_flags(orig_flags[0])


def flags(enabled=None, strategy=None):
    with __allow_nonbracketed_mutation():
        orig_flags = set_flags(enabled, strategy)
    try:
        yield
    finally:
        # recover the previous values
        with __allow_nonbracketed_mutation():
            set_flags(*orig_flags)

