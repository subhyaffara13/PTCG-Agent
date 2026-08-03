import os

def module_to_path(out_dir: str, module: str) -> str:
    fnam = os.path.join(out_dir, f"{module.replace('.', '/')}.pyi")
    if not os.path.exists(fnam):
        alt_fnam = fnam.replace(".pyi", "/__init__.pyi")
        if os.path.exists(alt_fnam):
            return alt_fnam
    return fnam

