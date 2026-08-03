import os
import subprocess

def _create_msvc_gs_stubs_lib(output_dir: str) -> str | None:
    """
    Create a static library with MSVC GS security symbol stubs for MinGW.

    Returns the library name (without lib prefix / .a suffix) if successful,
    or None on failure.
    """
    stubs_lib = os.path.join(output_dir, "libmsvc_gs_stubs.a")
    if os.path.exists(stubs_lib):
        return "msvc_gs_stubs"

    src_path = ""
    obj_path = ""
    try:
        src_path = os.path.join(output_dir, "_msvc_gs_stubs.c")
        obj_path = os.path.join(output_dir, "_msvc_gs_stubs.o")
        with open(src_path, "w") as f:
            f.write(_MSVC_GS_STUBS_SOURCE)

        mingw_gcc = MINGW_GXX.replace("g++", "gcc")
        subprocess.run(
            [mingw_gcc, "-c", src_path, "-o", obj_path],
            stderr=subprocess.PIPE,
            check=True,
        )
        mingw_ar = MINGW_GXX.replace("g++", "ar")
        subprocess.run(
            [mingw_ar, "rcs", stubs_lib, obj_path],
            stderr=subprocess.PIPE,
            check=True,
        )
        log.info("Created MSVC GS stubs library: %s", stubs_lib)
        return "msvc_gs_stubs"
    except (FileNotFoundError, subprocess.CalledProcessError):
        log.warning(
            "Failed to create MSVC GS stubs library.",
            exc_info=True,
        )
        if os.path.exists(stubs_lib):
            os.remove(stubs_lib)
        return None
    finally:
        for f in [src_path, obj_path]:
            if f and os.path.exists(f):
                os.remove(f)

