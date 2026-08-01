
def _generate_setup_py(build_dir: str, experimental: bool, opt_level: str) -> str:
    """Generate setup.py content for building librt directly.

    We inline LIBRT_MODULES/RUNTIME_C_FILES/include_dir/cflags values to avoid
    importing mypyc.build, which recursively imports lots of things.
    """
    lib_rt_dir = include_dir()

    # Get compiler flags using the shared helper
    cflags = get_cflags(opt_level=opt_level, experimental_features=experimental)

    # Serialize values to inline in generated setup.py
    librt_modules_repr = repr(
        [(m.module, m.c_files, m.other_files, m.include_dirs) for m in LIBRT_MODULES]
    )
    runtime_files_repr = repr(RUNTIME_C_FILES)
    cflags_repr = repr(cflags)

    return f"""\
import os
from setuptools import setup, Extension
import build_setup  # noqa: F401  # Monkey-patches compiler for per-file SIMD flags

build_dir = {build_dir!r}
lib_rt_dir = {lib_rt_dir!r}

RUNTIME_C_FILES = {runtime_files_repr}
LIBRT_MODULES = {librt_modules_repr}
CFLAGS = {cflags_repr}

def write_file(path, contents):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(contents)

# Copy runtime C files
for name in RUNTIME_C_FILES:
    src = os.path.join(lib_rt_dir, name)
    dst = os.path.join(build_dir, name)
    with open(src, "rb") as f:
        write_file(dst, f.read())

# Build extensions for each librt module
extensions = []
for mod, file_names, extra_files, includes in LIBRT_MODULES:
    # Copy source files
    for fname in file_names + extra_files:
        src = os.path.join(lib_rt_dir, fname)
        dst = os.path.join(build_dir, fname)
        with open(src, "rb") as f:
            write_file(dst, f.read())

    extensions.append(Extension(
        mod,
        sources=[os.path.join(build_dir, f) for f in file_names + RUNTIME_C_FILES],
        include_dirs=[lib_rt_dir] + [os.path.join(lib_rt_dir, d) for d in includes],
        extra_compile_args=CFLAGS,
    ))

setup(name='librt_cached', ext_modules=extensions)
"""

