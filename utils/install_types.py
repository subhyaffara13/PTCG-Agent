
def install_types(
    formatter: util.FancyFormatter,
    options: Options,
    *,
    after_run: bool = False,
    non_interactive: bool = False,
) -> bool:
    """Install stub packages using pip if some missing stubs were detected."""
    packages = read_types_packages_to_install(options.cache_dir, after_run)
    if not packages:
        # If there are no missing stubs, generate no output.
        return False
    if after_run and not non_interactive:
        print()
    print("Installing missing stub packages:")
    assert options.python_executable, "Python executable required to install types"
    cmd = [options.python_executable, "-m", "pip", "install"] + packages
    print(formatter.style(" ".join(cmd), "none", bold=True))
    print()
    if not non_interactive:
        x = input("Install? [yN] ")
        if not x.strip() or not x.lower().startswith("y"):
            print(formatter.style("mypy: Skipping installation", "red", bold=True))
            sys.exit(2)
        print()
    subprocess.run(cmd)
    return True

