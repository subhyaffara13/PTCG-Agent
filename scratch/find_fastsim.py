import glob, os
patterns = ["**/*.py", "**/*.cpp", "**/*.h"]
for pat in patterns:
    for f in glob.glob(pat, recursive=True):
        try:
            for i, l in enumerate(open(f, errors="ignore")):
                if "FAST_SIM" in l or "fast_sim" in l:
                    print(f"{f}:{i+1}: {l.rstrip()}")
        except Exception:
            pass
