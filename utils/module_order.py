
def module_order(errors: list[str]) -> list[str]:
    result = []
    seen = set()
    mods = []
    for e in errors:
        if ":" not in e:
            dump_original_errors(errors)
            pytest.fail(f"Only module scoped errors are supported, got {e}")
        mod, _ = e.split(":", maxsplit=1)
        mods.append(mod)
    for i, mod in enumerate(mods):
        if i > 0:
            if mod != mods[i - 1] and mod in seen:
                dump_original_errors(errors)
                pytest.fail(f"Each module must form a single block, {mod} appears split")
        if mod not in seen:
            result.append(mod)
            seen.add(mod)
    return result

