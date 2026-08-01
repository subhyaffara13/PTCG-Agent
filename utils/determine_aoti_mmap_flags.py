
def determine_aoti_mmap_flags(consts_size: int) -> tuple[bool, bool]:
    """
    Decide whether we should mmap weights, and whether to store the weights with .so.

    If force_mmap_weights or package_constants_on_disk_format == "binary_blob" configs are set, respect the config.

    Returns tuple (use_external_weights, use_mmap_weights).
    """

    if (
        config.aot_inductor.force_mmap_weights
        and config.aot_inductor.package_constants_on_disk_format == "binary_blob"
    ):
        raise RuntimeError(
            "config.aot_inductor.package_constants_on_disk_format = binary_blob and "
            "config.aot_inductor.force_mmap_weights cannot both be True."
        )

    if config.aot_inductor.force_mmap_weights:
        if config.aot_inductor.cross_target_platform == "windows":
            raise RuntimeError(
                "when cross_target_platform is windows, use_mmap_weights should not be true."
            )
        use_mmap_weights = True
        use_external_weights = False
        return use_external_weights, use_mmap_weights

    if config.aot_inductor.package_constants_on_disk_format == "binary_blob":
        use_external_weights = True
        use_mmap_weights = False
        return use_external_weights, use_mmap_weights

    if consts_size <= 2_000_000_000:
        return False, False

    use_external_weights = False
    use_mmap_weights = not config.is_fbcode()

    return use_external_weights, use_mmap_weights

