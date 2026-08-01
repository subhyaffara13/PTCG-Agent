
def cmd_check(args: argparse.Namespace) -> int:
    variants = load_variants(args.env)
    print(f"env: {args.env}")
    print(f"variants: {sorted(variants)}")

    # Baseline parity: BASELINE.make_prompt must equal harness.generate_prompt
    # for the same observation. Loaded via the per-env harness module.
    try:
        harness_mod_path = _variants_module_path(args.env).rsplit(".", 1)[0] + ".harness"
        harness_mod = importlib.import_module(harness_mod_path)
        prod_make_prompt = getattr(harness_mod, "generate_prompt", None)
    except ModuleNotFoundError:
        prod_make_prompt = None

    obs_list = _seeded_observations(args.env, n=args.parity_seeds)
    if not obs_list:
        print("  (could not build seeded observations -- skipping render check)")
        return 0

    failed = False

    baseline = variants["baseline"]
    if prod_make_prompt is None:
        print("  (no harness.generate_prompt found -- skipping baseline parity)")
    else:
        for i, obs in enumerate(obs_list):
            try:
                a = prod_make_prompt(obs, [])
                b = baseline.make_prompt(obs, [])
            except Exception as e:
                print(f"  baseline parity obs[{i}]: ERROR {e}")
                failed = True
                continue
            if a != b:
                print(f"  baseline parity obs[{i}]: MISMATCH")
                failed = True
            else:
                print(f"  baseline parity obs[{i}]: ok ({len(a)} chars)")

    # Render check: every variant must render without error on each obs.
    for name, variant in variants.items():
        for i, obs in enumerate(obs_list):
            try:
                prompt = variant.make_prompt(obs, [])
                assert isinstance(prompt, str) and prompt
            except Exception as e:
                print(f"  variant '{name}' obs[{i}]: RENDER ERROR {e}")
                traceback.print_exc()
                failed = True
        print(f"  variant '{name}': rendered ok across {len(obs_list)} observations")

    if failed:
        print("FAIL")
        return 1
    print("OK")
    return 0

