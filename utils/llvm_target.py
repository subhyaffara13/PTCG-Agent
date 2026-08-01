
def llvm_target() -> str:
    if sys.platform == "linux":
        cpuinfo = Path("/proc/cpuinfo").read_text()
        if "avx512" in cpuinfo:
            return "llvm -mcpu=skylake-avx512"
        elif "avx2" in cpuinfo:
            return "llvm -mcpu=core-avx2"
    return "llvm"

