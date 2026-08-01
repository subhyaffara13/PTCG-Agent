
def parseOptions(args):
    rawOptions, files = getopt.gnu_getopt(
        args,
        "ld:o:fvqht:x:sgim:z:baey:",
        [
            "unicodedata=",
            "recalc-timestamp",
            "no-recalc-timestamp",
            "flavor=",
            "version",
            "with-zopfli",
            "newline=",
            "optimize-font-speed",
        ],
    )

    options = Options(rawOptions, len(files))
    jobs = []

    if not files:
        raise getopt.GetoptError("Must specify at least one input file")

    for input in files:
        if input != "-" and not os.path.isfile(input):
            raise getopt.GetoptError('File not found: "%s"' % input)
        tp = guessFileType(input)
        if tp in ("OTF", "TTF", "TTC", "WOFF", "WOFF2"):
            extension = ".ttx"
            if options.listTables:
                action = ttList
            else:
                action = ttDump
        elif tp == "TTX":
            extension = "." + options.flavor if options.flavor else ".ttf"
            action = ttCompile
        elif tp == "OTX":
            extension = "." + options.flavor if options.flavor else ".otf"
            action = ttCompile
        else:
            raise getopt.GetoptError('Unknown file type: "%s"' % input)

        if options.outputFile:
            output = options.outputFile
        else:
            if input == "-":
                raise getopt.GetoptError("Must provide -o when reading from stdin")
            output = makeOutputFileName(
                input, options.outputDir, extension, options.overWrite
            )
            # 'touch' output file to avoid race condition in choosing file names
            if action != ttList:
                open(output, "a").close()
        jobs.append((action, input, output))
    return jobs, options


def parse_options(args: list[str]) -> Options:
    parser = argparse.ArgumentParser(
        prog="stubgen", usage=HEADER, description=DESCRIPTION, fromfile_prefix_chars="@"
    )

    parser.add_argument(
        "--ignore-errors",
        action="store_true",
        help="ignore errors when trying to generate stubs for modules",
    )
    parser.add_argument(
        "--no-import",
        action="store_true",
        help="don't import the modules, just parse and analyze them "
        "(doesn't work with C extension modules and might not "
        "respect __all__)",
    )
    parser.add_argument(
        "--no-analysis",
        "--parse-only",
        dest="parse_only",
        action="store_true",
        help="don't perform semantic analysis of sources, just parse them "
        "(only applies to Python modules, might affect quality of stubs. "
        "Not compatible with --inspect-mode)",
    )
    parser.add_argument(
        "--inspect-mode",
        dest="inspect",
        action="store_true",
        help="import and inspect modules instead of parsing source code."
        "This is the default behavior for c modules and pyc-only packages, but "
        "it is also useful for pure python modules with dynamically generated members.",
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="generate stubs for objects and members considered private "
        "(single leading underscore and no trailing underscores)",
    )
    parser.add_argument(
        "--export-less",
        action="store_true",
        help="don't implicitly export all names imported from other modules in the same package",
    )
    parser.add_argument(
        "--include-docstrings",
        action="store_true",
        help="include existing docstrings with the stubs",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="show more verbose messages")
    parser.add_argument("-q", "--quiet", action="store_true", help="show fewer messages")
    parser.add_argument(
        "--doc-dir",
        metavar="PATH",
        default="",
        help="use .rst documentation in PATH (this may result in "
        "better stubs in some cases; consider setting this to "
        "DIR/Python-X.Y.Z/Doc/library)",
    )
    parser.add_argument(
        "--search-path",
        metavar="PATH",
        default="",
        help="specify module search directories, separated by ':' "
        "(currently only used if --no-import is given)",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="PATH",
        dest="output_dir",
        default="out",
        help="change the output directory [default: %(default)s]",
    )
    parser.add_argument(
        "-m",
        "--module",
        action="append",
        metavar="MODULE",
        dest="modules",
        default=[],
        help="generate stub for module; can repeat for more modules",
    )
    parser.add_argument(
        "-p",
        "--package",
        action="append",
        metavar="PACKAGE",
        dest="packages",
        default=[],
        help="generate stubs for package recursively; can be repeated",
    )
    parser.add_argument(
        metavar="files",
        nargs="*",
        dest="files",
        help="generate stubs for given files or directories",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + mypy.version.__version__
    )

    ns = parser.parse_args(args)

    pyversion = sys.version_info[:2]
    ns.interpreter = sys.executable

    if ns.modules + ns.packages and ns.files:
        parser.error("May only specify one of: modules/packages or files.")
    if ns.quiet and ns.verbose:
        parser.error("Cannot specify both quiet and verbose messages")
    if ns.inspect and ns.parse_only:
        parser.error("Cannot specify both --parse-only/--no-analysis and --inspect-mode")

    # Create the output folder if it doesn't already exist.
    os.makedirs(ns.output_dir, exist_ok=True)

    return Options(
        pyversion=pyversion,
        no_import=ns.no_import,
        inspect=ns.inspect,
        doc_dir=ns.doc_dir,
        search_path=ns.search_path.split(":"),
        interpreter=ns.interpreter,
        ignore_errors=ns.ignore_errors,
        parse_only=ns.parse_only,
        include_private=ns.include_private,
        output_dir=ns.output_dir,
        modules=ns.modules,
        packages=ns.packages,
        files=ns.files,
        verbose=ns.verbose,
        quiet=ns.quiet,
        export_less=ns.export_less,
        include_docstrings=ns.include_docstrings,
    )


def parse_options(args: list[str]) -> _Arguments:
    parser = argparse.ArgumentParser(
        description="Compares stubs to objects introspected from the runtime."
    )
    parser.add_argument("modules", nargs="*", help="Modules to test")
    parser.add_argument(
        "--concise",
        action="store_true",
        help="Makes stubtest's output more concise, one line per error",
    )
    parser.add_argument(
        "--ignore-missing-stub",
        action="store_true",
        help="Ignore errors for stub missing things that are present at runtime",
    )
    parser.add_argument(
        "--ignore-positional-only",
        action="store_true",
        help="Ignore errors for whether an argument should or shouldn't be positional-only",
    )
    # TODO: Remove once PEP 800 is accepted
    parser.add_argument(
        "--ignore-disjoint-bases",
        action="store_true",
        help="Disable checks for PEP 800 @disjoint_base classes",
    )
    parser.add_argument(
        "--strict-type-check-only",
        action="store_true",
        help="Require @type_check_only on private types that are not present at runtime",
    )
    parser.add_argument(
        "--allowlist",
        "--whitelist",
        action="append",
        metavar="FILE",
        default=[],
        help=(
            "Use file as an allowlist. Can be passed multiple times to combine multiple "
            "allowlists. Allowlists can be created with --generate-allowlist. Allowlists "
            "support regular expressions."
        ),
    )
    parser.add_argument(
        "--generate-allowlist",
        "--generate-whitelist",
        action="store_true",
        help="Print an allowlist (to stdout) to be used with --allowlist",
    )
    parser.add_argument(
        "--ignore-unused-allowlist",
        "--ignore-unused-whitelist",
        action="store_true",
        help="Ignore unused allowlist entries",
    )
    parser.add_argument(
        "--mypy-config-file",
        metavar="FILE",
        help=("Use specified mypy config file to determine mypy plugins and mypy path"),
    )
    parser.add_argument(
        "--custom-typeshed-dir", metavar="DIR", help="Use the custom typeshed in DIR"
    )
    parser.add_argument(
        "--check-typeshed", action="store_true", help="Check all stdlib modules in typeshed"
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + mypy.version.__version__
    )
    parser.add_argument("--pdb", action="store_true", help="Invoke pdb on fatal error")
    parser.add_argument(
        "--show-traceback", "--tb", action="store_true", help="Show traceback on fatal error"
    )

    return parser.parse_args(args, namespace=_Arguments())


def parse_options(
    program_text: str, testcase: DataDrivenTestCase, incremental_step: int
) -> Options:
    """Parse comments like '# flags: --foo' in a test case."""
    options = Options()
    flags = re.search("# flags: (.*)$", program_text, flags=re.MULTILINE)
    if incremental_step > 1:
        flags2 = re.search(f"# flags{incremental_step}: (.*)$", program_text, flags=re.MULTILINE)
        if flags2:
            flags = flags2

    if flags:
        flag_list = flags.group(1).split()
        flag_list.append("--no-site-packages")  # the tests shouldn't need an installed Python
        targets, options = process_options(flag_list, require_targets=False)
        if targets:
            # TODO: support specifying targets via the flags pragma
            raise RuntimeError("Specifying targets via the flags pragma is not supported.")
        if "--show-error-codes" not in flag_list:
            options.hide_error_codes = True
    else:
        flag_list = []
        options = Options()
        options.error_summary = False
        options.hide_error_codes = True

    # Allow custom python version to override testfile_pyversion.
    if all(flag.split("=")[0] != "--python-version" for flag in flag_list):
        options.python_version = testfile_pyversion(testcase.file)

    if testcase.config.getoption("--mypy-verbose"):
        options.verbosity = testcase.config.getoption("--mypy-verbose")
    if testcase.config.getoption("--mypy-num-workers"):
        options.num_workers = testcase.config.getoption("--mypy-num-workers")

    return options

