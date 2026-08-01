
def write_safety_flag(egg_dir, safe) -> None:
    # Write or remove zip safety flag file(s)
    for flag, fn in safety_flags.items():
        fn = os.path.join(egg_dir, fn)
        if os.path.exists(fn):
            if safe is None or bool(safe) != flag:
                os.unlink(fn)
        elif safe is not None and bool(safe) == flag:
            with open(fn, 'wt', encoding="utf-8") as f:
                f.write('\n')

