
def enable_cpu_fuser(fn):
    def wrapper(*args, **kwargs):
        torch._C._jit_override_can_fuse_on_cpu_legacy(True)
        torch._C._jit_override_can_fuse_on_cpu(True)
        torch._C._jit_set_te_must_use_llvm_cpu(False)
        try:
            fn(*args, **kwargs)
        finally:
            torch._C._jit_override_can_fuse_on_cpu_legacy(False)
            torch._C._jit_override_can_fuse_on_cpu(False)
            torch._C._jit_set_te_must_use_llvm_cpu(True)
    return wrapper

