
def is_flash_attn_greater_or_equal_2_10() -> bool:
    warnings.warn(
        "`is_flash_attn_greater_or_equal_2_10` is deprecated and will be removed in v5.8. "
        "Please use `is_flash_attn_greater_or_equal(library_version='2.1.0')` instead if needed.",
        FutureWarning,
    )
    return is_flash_attn_greater_or_equal("2.1.0")

