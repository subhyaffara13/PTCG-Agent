import os
import subprocess

def _gen_mingw_import_lib(dll_path: str, def_path: str, import_lib_path: str) -> None:
    """Generate a MinGW import library (.a) from a DLL using gendef and dlltool."""
    dll_name = os.path.basename(dll_path)
    with open(def_path, "w") as def_file:
        subprocess.run(
            ["gendef", "-", dll_path],
            stdout=def_file,
            stderr=subprocess.PIPE,
            check=True,
        )

    subprocess.run(
        [
            "x86_64-w64-mingw32-dlltool",
            "-d",
            def_path,
            "-l",
            import_lib_path,
            "-D",
            dll_name,
        ],
        stderr=subprocess.PIPE,
        check=True,
    )
    log.info("Generated MinGW import library %s from %s", import_lib_path, dll_name)

