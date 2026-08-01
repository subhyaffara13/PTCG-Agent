
def _maybe_load_decompositions():
    if os.environ.get("PYTORCH_JIT", "1") == "1" and __debug__:
        from torch._decomp import decompositions_for_jvp  # noqa: F401

