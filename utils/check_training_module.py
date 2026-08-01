
def check_training_module():
    import_ortmodule_exception = None

    has_ortmodule = False
    try:
        from onnxruntime.training.ortmodule import ORTModule  # noqa: F401, PLC0415

        has_ortmodule = True
    except ImportError:
        # ORTModule not present
        has_ortmodule = False
    except Exception as e:
        # this may happen if Cuda is not installed, we want to raise it after
        # for any exception other than not having ortmodule, we want to continue
        # device version validation and raise the exception after.
        try:
            from onnxruntime.training.ortmodule._fallback import ORTModuleInitException  # noqa: PLC0415

            if isinstance(e, ORTModuleInitException):
                # ORTModule is present but not ready to run yet
                has_ortmodule = True
        except Exception:
            # ORTModule not present
            has_ortmodule = False

        if not has_ortmodule:
            import_ortmodule_exception = e

    # collect onnxruntime package name, version, and cuda version
    package_name, version, cuda_version = get_package_name_and_version_info()

    if has_ortmodule and cuda_version:
        try:
            # collect cuda library build info. the library info may not be available
            # when the build environment has none or multiple libraries installed
            try:
                from .build_and_package_info import cudart_version  # noqa: PLC0415
            except ImportError:
                warnings.warn("WARNING: failed to get cudart_version from onnxruntime build info.")
                cudart_version = None

            def print_build_package_info():
                warnings.warn(f"onnxruntime training package info: package_name: {package_name}")
                warnings.warn(f"onnxruntime training package info: __version__: {version}")
                warnings.warn(f"onnxruntime training package info: cuda_version: {cuda_version}")
                warnings.warn(f"onnxruntime build info: cudart_version: {cudart_version}")

            # collection cuda library info from current environment.
            from onnxruntime.capi.onnxruntime_collect_build_info import find_cudart_versions  # noqa: PLC0415

            local_cudart_versions = find_cudart_versions(build_env=False, build_cuda_version=cuda_version)
            if cudart_version and local_cudart_versions and cudart_version not in local_cudart_versions:
                print_build_package_info()
                warnings.warn("WARNING: failed to find cudart version that matches onnxruntime build info")
                warnings.warn(f"WARNING: found cudart versions: {local_cudart_versions}")
        except Exception as e:
            warnings.warn("WARNING: failed to collect onnxruntime version and build info")
            print(e)

    if import_ortmodule_exception:
        raise import_ortmodule_exception

    return has_ortmodule, package_name, version, cuda_version

