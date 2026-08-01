
def show_versions():
    """
    Display useful system and dependencies information.

    When reporting issues, please include this information.
    """
    print("System settings")
    print("---------------")
    sys_info = _get_sys_info()
    print(
        "\n".join(
            f"{k:>{max(map(len, sys_info.keys())) + 1}}: {v}"
            for k, v in sys_info.items()
        )
    )

    print()
    print("Python dependencies")
    print("-------------------")
    deps_info = _get_deps_info()
    print(
        "\n".join(
            f"{k:>{max(map(len, deps_info.keys())) + 1}}: {v}"
            for k, v in deps_info.items()
        )
    )


def show_versions(as_json: str | bool = False) -> None:
    """
    Provide useful information, important for bug reports.

    It comprises info about hosting operation system, pandas version,
    and versions of other installed relative packages.

    Parameters
    ----------
    as_json : str or bool, default False
        * If False, outputs info in a human readable form to the console.
        * If str, it will be considered as a path to a file.
          Info will be written to that file in JSON format.
        * If True, outputs info in JSON format to the console.

    See Also
    --------
    get_option : Retrieve the value of the specified option.
    set_option : Set the value of the specified option or options.

    Examples
    --------
    >>> pd.show_versions()  # doctest: +SKIP
    Your output may look something like this:
    INSTALLED VERSIONS
    ------------------
    commit           : 37ea63d540fd27274cad6585082c91b1283f963d
    python           : 3.10.6.final.0
    python-bits      : 64
    OS               : Linux
    OS-release       : 5.10.102.1-microsoft-standard-WSL2
    Version          : #1 SMP Wed Mar 2 00:30:59 UTC 2022
    machine          : x86_64
    processor        : x86_64
    byteorder        : little
    LC_ALL           : None
    LANG             : en_GB.UTF-8
    LOCALE           : en_GB.UTF-8
    pandas           : 2.0.1
    numpy            : 1.24.3
    ...
    """
    sys_info = _get_sys_info()
    deps = _get_dependency_info()

    if as_json:
        j = {"system": sys_info, "dependencies": deps}

        if as_json is True:
            sys.stdout.writelines(json.dumps(j, indent=2))
        else:
            assert isinstance(as_json, str)  # needed for mypy
            with open(as_json, "w", encoding="utf-8") as f:
                json.dump(j, f, indent=2)

    else:
        assert isinstance(sys_info["LOCALE"], dict)  # needed for mypy
        language_code = sys_info["LOCALE"]["language-code"]
        encoding = sys_info["LOCALE"]["encoding"]
        sys_info["LOCALE"] = f"{language_code}.{encoding}"

        maxlen = max(len(x) for x in deps)
        print("\nINSTALLED VERSIONS")
        print("------------------")
        for k, v in sys_info.items():
            print(f"{k:<{maxlen}}: {v}")
        print("")
        for k, v in deps.items():
            print(f"{k:<{maxlen}}: {v}")

