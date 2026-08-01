
def find_library_location(lib_name: str) -> Path:
    # return the shared library file in the installed folder if exist,
    # else the file in the build folder
    torch_root = Path(torch.__file__).resolve().parent
    path = torch_root / 'lib' / lib_name
    if os.path.exists(path):
        return path
    torch_root = Path(__file__).resolve().parents[2]
    return torch_root / 'build' / 'lib' / lib_name

