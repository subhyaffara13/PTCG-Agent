
def _wrap_sycl_host_flags(cflags):
    host_cflags = []
    host_cxx = get_cxx_compiler()
    if IS_WINDOWS:
        for flag in cflags:
            if flag.startswith("-I"):
                flag = flag.replace("\\", "\\\\").replace("-I", "/I")
            else:
                flag = flag.replace("-D", "/D")
            flag = flag.replace('"', '\\"')
            host_cflags.append(flag)
        joined_host_cflags = ' '.join(host_cflags)

        external_include = _join_sycl_home("include").replace("\\", "\\\\")

        # Some versions of DPC++ compiler pass paths to SYCL headers as user include paths (`-I`) rather
        # than system paths (`-isystem`). This makes host compiler to report warnings encountered in the
        # SYCL headers, such as deprecated warnings, even if warmed API is not actually used in the program.
        # We expect that this issue will be addressed in the later version of DPC++ compiler. To workaround the
        # issue now we wrap paths to SYCL headers in `/external:I`. Warning free compilation is especially important
        # for Windows build as `/sdl` compilation flag assumes that and we will fail compilation otherwise.
        wrapped_host_cflags = [
            f"-fsycl-host-compiler={host_cxx}",
            f'-fsycl-host-compiler-options="\\"/external:I{external_include}\\" /external:W0 {joined_host_cflags}"',
        ]
    else:
        joined_host_cflags = ' '.join(cflags)
        wrapped_host_cflags = [
            f"-fsycl-host-compiler={host_cxx}",
            shlex.quote(f"-fsycl-host-compiler-options={joined_host_cflags}"),
        ]
    return wrapped_host_cflags

