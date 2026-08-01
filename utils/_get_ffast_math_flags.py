
def _get_ffast_math_flags() -> list[str]:
    if _IS_WINDOWS:
        flags = []
    else:
        # ffast-math is equivalent to these flags as in
        # https://github.com/gcc-mirror/gcc/blob/4700ad1c78ccd7767f846802fca148b2ea9a1852/gcc/opts.cc#L3458-L3468
        # however gcc<13 sets the FTZ/DAZ flags for runtime on x86 even if we have
        # -ffast-math -fno-unsafe-math-optimizations because the flags for runtime
        # are added by linking in crtfastmath.o. This is done by the spec file which
        # only does globbing for -ffast-math.
        flags = [
            "fno-trapping-math",
            "funsafe-math-optimizations",
            "ffinite-math-only",
            "fno-signed-zeros",
            "fno-math-errno",
        ]

        flags.append("fno-finite-math-only")
        if not config.cpp.enable_unsafe_math_opt_flag:
            flags.append("fno-unsafe-math-optimizations")
        flags.append(f"ffp-contract={config.cpp.enable_floating_point_contract_flag}")

        if is_gcc():
            flags.append("fexcess-precision=fast")

    return flags

