
def load_variants(env_name: str) -> dict[str, GameHarness]:
    """Return the ``VARIANTS`` registry for ``env_name``, or raise."""
    module_path = _variants_module_path(env_name)
    try:
        module = importlib.import_module(module_path)
    except ModuleNotFoundError as e:
        raise SystemExit(
            f"No prompt_variants.py found for env '{env_name}' "
            f"(expected at {module_path}). Bootstrap one with the "
            f"run-ablation skill."
        ) from e
    variants = getattr(module, "VARIANTS", None)
    if not isinstance(variants, dict) or not variants:
        raise SystemExit(
            f"{module_path} must expose a non-empty VARIANTS "
            f"dict[str, GameHarness]."
        )
    if "baseline" not in variants:
        raise SystemExit(
            f"{module_path}.VARIANTS must include a 'baseline' entry "
            f"(byte-identical to harness.py)."
        )
    return variants

