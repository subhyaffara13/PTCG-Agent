
def maybe_aoti_standalone_config(config_patches: dict[str, Any]) -> dict[str, Any]:
    """
    Ensures the configuration is internally consistent for standalone AOTInductor.

    If `aot_inductor_mode.compile_standalone` is set to True in the provided
    `config_patches` (or falls back to the global config), this function ensures
    that the following configs are also enabled:
        - `aot_inductor.package_cpp_only`

    Args:
        config_patches (dict[str, Any]): A dictionary of user-provided config
            overrides for AOTInductor compilation.

    Returns:
        dict[str, Any]: The possibly-updated `config_patches` dictionary.
    """

    def patch_config(
        config_patches: dict[str, Any], config_name: str, config_value: Any
    ) -> None:
        value = config_patches.get(config_name, getattr(config, config_name))
        if value is None:
            config_patches[config_name] = config_value
        elif not value and value != config_value:
            raise RuntimeError(
                f"Invalid config: {config_name}={config_value} when aot_inductor_mode.compile_standalone is True."
            )

    def force_patch_config(
        config_patches: dict[str, Any], config_name: str, config_value: Any
    ) -> None:
        value = config_patches.get(config_name, getattr(config, config_name))
        if value != config_value:
            log.warning(
                "Overriding: %s=%s when aot_inductor_mode.compile_standalone is True.",
                config_name,
                config_value,
            )
        config_patches[config_name] = config_value

    compile_standalone = config_patches.get(
        "aot_inductor_mode.compile_standalone",
        config.aot_inductor_mode.compile_standalone,
    )
    # Make a copy of the config_patches to avoid modifying the original dictionary, needed for testing
    config_patches = config_patches.copy()
    if compile_standalone:
        # Standlaone AOTInductor means only generate cpp project for building a standalone binary
        patch_config(config_patches, "aot_inductor.package_cpp_only", True)
        # Standlaone AOTInductor needs to embed the kernel code in the binary
        patch_config(config_patches, "aot_inductor.embed_kernel_binary", True)
        # Default to use multi-arch kernel codegen for non-rocm GPU
        patch_config(
            config_patches, "aot_inductor.emit_multi_arch_kernel", not torch.version.hip
        )
        patch_config(
            config_patches, "aot_inductor.model_name_for_generated_files", "aoti_model"
        )
        # TODO: change these two configs to default to None and use patch_config
        force_patch_config(
            config_patches,
            "aot_inductor.link_libtorch",
            config.test_configs.use_libtorch,
        )
        force_patch_config(config_patches, "aot_inductor.dynamic_linkage", False)

    cross_target_platform = config_patches.get(
        "aot_inductor.cross_target_platform",
        config.aot_inductor.cross_target_platform,
    )

    package_constants_in_so = config_patches.get(
        "aot_inductor.package_constants_in_so",
        config.aot_inductor.package_constants_in_so,
    )

    if cross_target_platform == "windows" and package_constants_in_so:
        raise RuntimeError(
            "config.aot_inductor.package_constants_in_so is not supported for windows cross-compilation. "
            "Please use config.aot_inductor.package_constants_on_disk_format = binary_blob."
        )

    return config_patches

