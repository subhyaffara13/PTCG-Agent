
def define_options(
    program: str = "mypy",
    header: str = HEADER,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
    server_options: bool = False,
) -> tuple[CapturableArgumentParser, list[str], list[tuple[str, bool]]]:
    """Define the options in the parser (by calling a bunch of methods that express/build our desired command-line flags).
    Returns a tuple of:
      a parser object, that can parse command line arguments to mypy (expected consumer: main's process_options),
      a list of what flags are strict (expected consumer: docs' html_builder's _add_strict_list),
      strict_flag_assignments (expected consumer: main's process_options)."""
    parser = CapturableArgumentParser(
        prog=program,
        usage=header,
        description=DESCRIPTION,
        epilog=FOOTER,
        fromfile_prefix_chars="@",
        formatter_class=AugmentedHelpFormatter,
        add_help=False,
        stdout=stdout,
        stderr=stderr,
    )

    strict_flag_names: list[str] = []
    strict_flag_assignments: list[tuple[str, bool]] = []

    def add_invertible_flag(
        flag: str,
        *,
        inverse: str | None = None,
        default: bool,
        dest: str | None = None,
        help: str,
        strict_flag: bool = False,
        group: argparse._ActionsContainer | None = None,
    ) -> None:
        if inverse is None:
            inverse = invert_flag_name(flag)
        if group is None:
            group = parser

        if help is not argparse.SUPPRESS:
            help += f" (inverse: {inverse})"

        arg = group.add_argument(
            flag, action="store_false" if default else "store_true", dest=dest, help=help
        )
        dest = arg.dest
        group.add_argument(
            inverse,
            action="store_true" if default else "store_false",
            dest=dest,
            help=argparse.SUPPRESS,
        )
        if strict_flag:
            assert dest is not None
            strict_flag_names.append(flag)
            strict_flag_assignments.append((dest, not default))

    # Unless otherwise specified, arguments will be parsed directly onto an
    # Options object.  Options that require further processing should have
    # their `dest` prefixed with `special-opts:`, which will cause them to be
    # parsed into the separate special_opts namespace object.

    # Our style guide for formatting the output of running `mypy --help`:
    # Flags:
    # 1.  The flag help text should start with a capital letter but never end with a period.
    # 2.  Keep the flag help text brief -- ideally just a single sentence.
    # 3.  All flags must be a part of a group, unless the flag is deprecated or suppressed.
    # 4.  Avoid adding new flags to the "miscellaneous" groups -- instead add them to an
    #     existing group or, if applicable, create a new group. Feel free to move existing
    #     flags to a new group: just be sure to also update the documentation to match.
    #
    # Groups:
    # 1.  The group title and description should start with a capital letter.
    # 2.  The first sentence of a group description should be written in the bare infinitive.
    #     Tip: try substituting the group title and description into the following sentence:
    #     > {group_title}: these flags will {group_description}
    #     Feel free to add subsequent sentences that add additional details.
    # 3.  If you cannot think of a meaningful description for a new group, omit it entirely.
    #     (E.g. see the "miscellaneous" sections).
    # 4.  The text of the group description should end with a period, optionally followed
    #     by a documentation reference (URL).
    # 5.  If you want to include a documentation reference, place it at the end of the
    #     description. Feel free to open with a brief reference ("See also:", "For more
    #     information:", etc.), followed by a space, then the entire URL including
    #     "https://" scheme identifier and fragment ("#some-target-heading"), if any.
    #     Do not end with a period (or any other characters not part of the URL).
    #     URLs longer than the available terminal width will overflow without being
    #     broken apart. This facilitates both URL detection, and manual copy-pasting.

    general_group = parser.add_argument_group(title="Optional arguments")
    general_group.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit"
    )
    general_group.add_argument(
        "-v", "--verbose", action="count", dest="verbosity", help="More verbose messages"
    )

    compilation_status = "no" if __file__.endswith(".py") else "yes"
    general_group.add_argument(
        "-V",
        "--version",
        action=CapturableVersionAction,
        version="%(prog)s " + __version__ + f" (compiled: {compilation_status})",
        help="Show program's version number and exit",
        stdout=stdout,
    )

    general_group.add_argument(
        "-O",
        "--output",
        metavar="FORMAT",
        help="Set a custom output format",
        choices=OUTPUT_CHOICES,
    )

    config_group = parser.add_argument_group(
        title="Config file",
        description="Use a config file instead of command line arguments. "
        "This is useful if you are using many flags or want "
        "to set different options per each module.",
    )
    config_group.add_argument(
        "--config-file",
        help=(
            f"Configuration file, must have a [mypy] section "
            f"(defaults to {', '.join(defaults.CONFIG_NAMES + defaults.SHARED_CONFIG_NAMES)})"
        ),
    )
    add_invertible_flag(
        "--warn-unused-configs",
        default=False,
        help="Warn about unused '[mypy-<pattern>]' or '[[tool.mypy.overrides]]' config sections",
        group=config_group,
    )

    imports_group = parser.add_argument_group(
        title="Import discovery", description="Configure how imports are discovered and followed."
    )
    add_invertible_flag(
        "--no-namespace-packages",
        dest="namespace_packages",
        default=True,
        help="Disable support for namespace packages (PEP 420, __init__.py-less)",
        group=imports_group,
    )
    imports_group.add_argument(
        "--ignore-missing-imports",
        action="store_true",
        help="Silently ignore imports of missing modules",
    )
    imports_group.add_argument(
        "--follow-untyped-imports",
        action="store_true",
        help="Typecheck modules without stubs or py.typed marker",
    )
    imports_group.add_argument(
        "--follow-imports",
        choices=["normal", "silent", "skip", "error"],
        default="normal",
        help="How to treat imports (default normal)",
    )
    imports_group.add_argument(
        "--python-executable",
        action="store",
        metavar="EXECUTABLE",
        help="Python executable used for finding PEP 561 compliant installed packages and stubs",
        dest="special-opts:python_executable",
    )
    imports_group.add_argument(
        "--no-site-packages",
        action="store_true",
        dest="special-opts:no_executable",
        help="Do not search for installed PEP 561 compliant packages",
    )
    imports_group.add_argument(
        "--no-silence-site-packages",
        action="store_true",
        help="Do not silence errors in PEP 561 compliant installed packages",
    )

    platform_group = parser.add_argument_group(
        title="Platform configuration",
        description="Type check code assuming it will be run under certain "
        "runtime conditions. By default, mypy assumes your code "
        "will be run using the same operating system and Python "
        "version you are using to run mypy itself.",
    )
    platform_group.add_argument(
        "--python-version",
        type=parse_version,
        metavar="x.y",
        help="Type check code assuming it will be running on Python x.y",
        dest="special-opts:python_version",
    )
    platform_group.add_argument(
        "--platform",
        action="store",
        metavar="PLATFORM",
        help="Type check special-cased code for the given OS platform (defaults to sys.platform)",
    )
    platform_group.add_argument(
        "--always-true",
        metavar="NAME",
        action="append",
        default=[],
        help="Additional variable to be considered True (may be repeated)",
    )
    platform_group.add_argument(
        "--always-false",
        metavar="NAME",
        action="append",
        default=[],
        help="Additional variable to be considered False (may be repeated)",
    )

    disallow_any_group = parser.add_argument_group(
        title="Disallow dynamic typing",
        description="Disallow the use of the dynamic 'Any' type under certain conditions.",
    )
    disallow_any_group.add_argument(
        "--disallow-any-expr",
        default=False,
        action="store_true",
        help="Disallow all expressions that have type Any",
    )
    disallow_any_group.add_argument(
        "--disallow-any-decorated",
        default=False,
        action="store_true",
        help="Disallow functions that have Any in their signature after decorator transformation",
    )
    disallow_any_group.add_argument(
        "--disallow-any-explicit",
        default=False,
        action="store_true",
        help="Disallow explicit Any in type positions",
    )
    add_invertible_flag(
        "--disallow-any-generics",
        default=False,
        strict_flag=True,
        help="Disallow usage of generic types that do not specify explicit type parameters",
        group=disallow_any_group,
    )
    add_invertible_flag(
        "--disallow-any-unimported",
        default=False,
        help="Disallow Any types resulting from unfollowed imports",
        group=disallow_any_group,
    )
    add_invertible_flag(
        "--disallow-subclassing-any",
        default=False,
        strict_flag=True,
        help="Disallow subclassing values of type 'Any' when defining classes",
        group=disallow_any_group,
    )

    untyped_group = parser.add_argument_group(
        title="Untyped definitions and calls",
        description="Configure how untyped definitions and calls are handled. "
        "Note: by default, mypy ignores any untyped function definitions "
        "and assumes any calls to such functions have a return "
        "type of 'Any'.",
    )
    add_invertible_flag(
        "--disallow-untyped-calls",
        default=False,
        strict_flag=True,
        help="Disallow calling functions without type annotations"
        " from functions with type annotations",
        group=untyped_group,
    )
    untyped_group.add_argument(
        "--untyped-calls-exclude",
        metavar="MODULE",
        action="append",
        default=[],
        help="Disable --disallow-untyped-calls for functions/methods coming"
        " from specific package, module, or class",
    )
    add_invertible_flag(
        "--disallow-untyped-defs",
        default=False,
        strict_flag=True,
        help="Disallow defining functions without type annotations"
        " or with incomplete type annotations",
        group=untyped_group,
    )
    add_invertible_flag(
        "--disallow-incomplete-defs",
        default=False,
        strict_flag=True,
        help="Disallow defining functions with incomplete type annotations "
        "(while still allowing entirely unannotated definitions)",
        group=untyped_group,
    )
    add_invertible_flag(
        "--check-untyped-defs",
        default=False,
        strict_flag=True,
        help="Type check the interior of functions without type annotations",
        group=untyped_group,
    )
    add_invertible_flag(
        "--disallow-untyped-decorators",
        default=False,
        strict_flag=True,
        help="Disallow decorating typed functions with untyped decorators",
        group=untyped_group,
    )

    none_group = parser.add_argument_group(
        title="None and Optional handling",
        description="Adjust how values of type 'None' are handled. For more context on "
        "how mypy handles values of type 'None', see: "
        "https://mypy.readthedocs.io/en/stable/kinds_of_types.html#optional-types-and-the-none-type",
    )
    add_invertible_flag(
        "--implicit-optional",
        default=False,
        help="Assume arguments with default values of None are Optional",
        group=none_group,
    )
    none_group.add_argument("--strict-optional", action="store_true", help=argparse.SUPPRESS)
    none_group.add_argument(
        "--no-strict-optional",
        action="store_false",
        dest="strict_optional",
        help="Disable strict Optional checks (inverse: --strict-optional)",
    )

    lint_group = parser.add_argument_group(
        title="Configuring warnings",
        description="Detect code that is sound but redundant or problematic.",
    )
    add_invertible_flag(
        "--warn-redundant-casts",
        default=False,
        strict_flag=True,
        help="Warn about casting an expression to its inferred type",
        group=lint_group,
    )
    add_invertible_flag(
        "--warn-unused-ignores",
        default=False,
        strict_flag=True,
        help="Warn about unneeded '# type: ignore' comments",
        group=lint_group,
    )
    add_invertible_flag(
        "--no-warn-no-return",
        dest="warn_no_return",
        default=True,
        help="Do not warn about functions that end without returning",
        group=lint_group,
    )
    add_invertible_flag(
        "--warn-return-any",
        default=False,
        strict_flag=True,
        help="Warn about returning values of type Any from non-Any typed functions",
        group=lint_group,
    )
    add_invertible_flag(
        "--warn-unreachable",
        default=False,
        strict_flag=False,
        help="Warn about statements or expressions inferred to be unreachable",
        group=lint_group,
    )
    add_invertible_flag(
        "--report-deprecated-as-note",
        default=False,
        strict_flag=False,
        help="Report importing or using deprecated features as notes instead of errors",
        group=lint_group,
    )
    lint_group.add_argument(
        "--deprecated-calls-exclude",
        metavar="MODULE",
        action="append",
        default=[],
        help="Disable deprecated warnings for functions/methods coming"
        " from specific package, module, or class",
    )

    # Note: this group is intentionally added here even though we don't add
    # --strict to this group near the end.
    #
    # That way, this group will appear after the various strictness groups
    # but before the remaining flags.
    # We add `--strict` near the end so we don't accidentally miss any strictness
    # flags that are added after this group.
    strictness_group = parser.add_argument_group(title="Miscellaneous strictness flags")

    add_invertible_flag(
        "--allow-untyped-globals",
        default=False,
        strict_flag=False,
        help="Suppress toplevel errors caused by missing annotations",
        group=strictness_group,
    )

    add_invertible_flag(
        "--allow-redefinition",
        default=False,
        strict_flag=False,
        help="Allow flexible variable redefinition with a new type",
        group=strictness_group,
    )

    add_invertible_flag(
        "--allow-redefinition-old",
        default=False,
        strict_flag=False,
        help="Allow restricted, unconditional variable redefinition with a new type",
        group=strictness_group,
    )

    add_invertible_flag(
        "--allow-redefinition-new",
        default=False,
        strict_flag=False,
        help="Deprecated alias for --allow-redefinition",
        group=strictness_group,
        dest="allow_redefinition",
    )

    add_invertible_flag(
        "--no-implicit-reexport",
        default=True,
        strict_flag=True,
        dest="implicit_reexport",
        help="Treat imports as private unless aliased",
        group=strictness_group,
    )

    add_invertible_flag(
        "--strict-equality",
        default=False,
        strict_flag=True,
        help="Prohibit equality, identity, and container checks for non-overlapping types "
        "(except `None`)",
        group=strictness_group,
    )

    add_invertible_flag(
        "--strict-equality-for-none",
        default=False,
        strict_flag=False,
        help="Extend `--strict-equality` for `None` checks",
        group=strictness_group,
    )

    add_invertible_flag(
        "--no-strict-bytes",
        default=True,
        dest="strict_bytes",
        help="Treat bytearray and memoryview as subtypes of bytes",
        group=strictness_group,
    )

    add_invertible_flag(
        "--extra-checks",
        default=False,
        strict_flag=True,
        help="Enable additional checks that are technically correct but may be impractical "
        "in real code. For example, this prohibits partial overlap in TypedDict updates, "
        "and makes arguments prepended via Concatenate positional-only",
        group=strictness_group,
    )

    strict_help = "Strict mode; enables the following flags: {}".format(
        ", ".join(strict_flag_names)
    )
    strictness_group.add_argument(
        "--strict", action="store_true", dest="special-opts:strict", help=strict_help
    )

    strictness_group.add_argument(
        "--disable-error-code",
        metavar="NAME",
        action="append",
        default=[],
        help="Disable a specific error code",
    )
    strictness_group.add_argument(
        "--enable-error-code",
        metavar="NAME",
        action="append",
        default=[],
        help="Enable a specific error code",
    )

    error_group = parser.add_argument_group(
        title="Configuring error messages",
        description="Adjust the amount of detail shown in error messages.",
    )
    add_invertible_flag(
        "--show-error-context",
        default=False,
        dest="show_error_context",
        help='Precede errors with "note:" messages explaining context',
        group=error_group,
    )
    add_invertible_flag(
        "--show-column-numbers",
        default=False,
        help="Show column numbers in error messages",
        group=error_group,
    )
    add_invertible_flag(
        "--show-error-end",
        default=False,
        help="Show end line/end column numbers in error messages."
        " This implies --show-column-numbers",
        group=error_group,
    )
    add_invertible_flag(
        "--hide-error-codes",
        default=False,
        help="Hide error codes in error messages",
        group=error_group,
    )
    add_invertible_flag(
        "--show-error-code-links",
        default=False,
        help="Show links to error code documentation",
        group=error_group,
    )
    add_invertible_flag(
        "--pretty",
        default=False,
        help="Use visually nicer output in error messages:"
        " Use soft word wrap, show source code snippets,"
        " and show error location markers",
        group=error_group,
    )
    add_invertible_flag(
        "--no-color-output",
        dest="color_output",
        default=True,
        help="Do not colorize error messages",
        group=error_group,
    )
    add_invertible_flag(
        "--no-error-summary",
        dest="error_summary",
        default=True,
        help="Do not show error stats summary",
        group=error_group,
    )
    add_invertible_flag(
        "--show-absolute-path",
        default=False,
        help="Show absolute paths to files",
        group=error_group,
    )
    error_group.add_argument(
        "--soft-error-limit",
        default=defaults.MANY_ERRORS_THRESHOLD,
        type=int,
        dest="many_errors_threshold",
        help=argparse.SUPPRESS,
    )

    incremental_group = parser.add_argument_group(
        title="Incremental mode",
        description="Adjust how mypy incrementally type checks and caches modules. "
        "Mypy caches type information about modules into a cache to "
        "let you speed up future invocations of mypy. Also see "
        "mypy's daemon mode: "
        "https://mypy.readthedocs.io/en/stable/mypy_daemon.html#mypy-daemon",
    )
    incremental_group.add_argument(
        "-i", "--incremental", action="store_true", help=argparse.SUPPRESS
    )
    incremental_group.add_argument(
        "--no-incremental",
        action="store_false",
        dest="incremental",
        help="Disable module cache (inverse: --incremental)",
    )
    incremental_group.add_argument(
        "--cache-dir",
        action="store",
        metavar="DIR",
        help="Store module cache info in the given folder in incremental mode "
        "(defaults to '{}')".format(defaults.CACHE_DIR),
    )
    add_invertible_flag(
        "--sqlite-cache",
        default=False,
        help="Use a sqlite database to store the cache",
        group=incremental_group,
    )
    incremental_group.add_argument(
        "--sqlite-num-shards",
        type=int,
        default=defaults.SQLITE_NUM_SHARDS,
        dest="sqlite_num_shards",
        help=argparse.SUPPRESS,
    )
    incremental_group.add_argument(
        "--cache-fine-grained",
        action="store_true",
        help="Include fine-grained dependency information in the cache for the mypy daemon",
    )
    add_invertible_flag(
        "--no-fixed-format-cache",
        dest="fixed_format_cache",
        default=True,
        help="Do not use new fixed format cache",
        group=incremental_group,
    )
    incremental_group.add_argument(
        "--skip-version-check",
        action="store_true",
        help="Allow using cache written by older mypy version",
    )
    incremental_group.add_argument(
        "--skip-cache-mtime-checks",
        action="store_true",
        help="Skip cache internal consistency checks based on mtime",
    )

    internals_group = parser.add_argument_group(
        title="Advanced options", description="Debug and customize mypy internals."
    )
    internals_group.add_argument("--pdb", action="store_true", help="Invoke pdb on fatal error")
    internals_group.add_argument(
        "--show-traceback", "--tb", action="store_true", help="Show traceback on fatal error"
    )
    internals_group.add_argument(
        "--raise-exceptions", action="store_true", help="Raise exception on fatal error"
    )
    internals_group.add_argument(
        "--custom-typing-module",
        metavar="MODULE",
        dest="custom_typing_module",
        help="Use a custom typing module",
    )
    internals_group.add_argument(
        "--old-type-inference", action="store_true", help=argparse.SUPPRESS
    )
    internals_group.add_argument(
        "--disable-expression-cache", action="store_true", help=argparse.SUPPRESS
    )
    parser.add_argument(
        "--enable-incomplete-feature",
        action="append",
        metavar="{" + ",".join(sorted(INCOMPLETE_FEATURES)) + "}",
        help="Enable support of incomplete/experimental features for early preview",
    )
    internals_group.add_argument(
        "--custom-typeshed-dir", metavar="DIR", help="Use the custom typeshed in DIR"
    )
    add_invertible_flag(
        "--warn-incomplete-stub",
        default=False,
        help="Warn if missing type annotation in typeshed, only relevant with"
        " --disallow-untyped-defs or --disallow-incomplete-defs enabled",
        group=internals_group,
    )
    internals_group.add_argument(
        "--shadow-file",
        nargs=2,
        metavar=("SOURCE_FILE", "SHADOW_FILE"),
        dest="shadow_file",
        action="append",
        help="When encountering SOURCE_FILE, read and type check "
        "the contents of SHADOW_FILE instead.",
    )
    internals_group.add_argument("--fast-exit", action="store_true", help=argparse.SUPPRESS)
    internals_group.add_argument(
        "--no-fast-exit", action="store_false", dest="fast_exit", help=argparse.SUPPRESS
    )
    # This flag is useful for mypy tests, where function bodies may be omitted. Plugin developers
    # may want to use this as well in their tests.
    add_invertible_flag(
        "--allow-empty-bodies", default=False, help=argparse.SUPPRESS, group=internals_group
    )
    # This undocumented feature exports limited line-level dependency information.
    internals_group.add_argument("--export-ref-info", action="store_true", help=argparse.SUPPRESS)

    # Experimental parallel type-checking support.
    internals_group.add_argument(
        "-n",
        "--num-workers",
        type=int,
        default=0,
        help="Number of separate mypy worker processes (experimental)",
    )

    report_group = parser.add_argument_group(
        title="Report generation", description="Generate a report in the specified format."
    )
    for report_type in sorted(defaults.REPORTER_NAMES):
        if report_type not in {"memory-xml"}:
            report_group.add_argument(
                f"--{report_type.replace('_', '-')}-report",
                metavar="DIR",
                dest=f"special-opts:{report_type}_report",
            )

    # Undocumented mypyc feature: generate annotated HTML source file
    report_group.add_argument(
        "-a", dest="mypyc_annotation_file", type=str, default=None, help=argparse.SUPPRESS
    )
    # Hidden mypyc feature: do not write any C files (keep existing ones and assume they exist).
    # This can be useful when debugging mypyc bugs.
    report_group.add_argument(
        "--skip-c-gen", dest="mypyc_skip_c_generation", action="store_true", help=argparse.SUPPRESS
    )

    misc_group = parser.add_argument_group(title="Miscellaneous")
    misc_group.add_argument("--quickstart-file", help=argparse.SUPPRESS)
    misc_group.add_argument(
        "--junit-xml",
        metavar="JUNIT_XML_OUTPUT_FILE",
        help="Write a JUnit XML test result document with type checking results to the given file",
    )
    misc_group.add_argument(
        "--junit-format",
        choices=["global", "per_file"],
        default="global",
        help="If --junit-xml is set, specifies format. global (default): single test with all errors; per_file: one test entry per file with failures",
    )
    misc_group.add_argument(
        "--find-occurrences",
        metavar="CLASS.MEMBER",
        dest="special-opts:find_occurrences",
        help="Print out all usages of a class member (experimental)",
    )
    misc_group.add_argument(
        "--scripts-are-modules",
        action="store_true",
        help="Script x becomes module x instead of __main__",
    )

    add_invertible_flag(
        "--install-types",
        default=False,
        strict_flag=False,
        help="Install detected missing library stub packages using pip",
        group=misc_group,
    )
    add_invertible_flag(
        "--non-interactive",
        default=False,
        strict_flag=False,
        help=(
            "Install stubs without asking for confirmation and hide "
            + "errors, with --install-types"
        ),
        group=misc_group,
        inverse="--interactive",
    )

    if server_options:
        misc_group.add_argument(
            "--use-fine-grained-cache",
            action="store_true",
            help="Use the cache in fine-grained incremental mode",
        )

    # hidden options
    parser.add_argument(
        "--stats", action="store_true", dest="dump_type_stats", help=argparse.SUPPRESS
    )
    parser.add_argument(
        "--inferstats", action="store_true", dest="dump_inference_stats", help=argparse.SUPPRESS
    )
    parser.add_argument("--dump-build-stats", action="store_true", help=argparse.SUPPRESS)
    # Dump timing stats for each processed file into the given output file
    parser.add_argument("--timing-stats", dest="timing_stats", help=argparse.SUPPRESS)
    # Dump per line type checking timing stats for each processed file into the given
    # output file. Only total time spent in each top level expression will be shown.
    # Times are show in microseconds.
    parser.add_argument(
        "--line-checking-stats", dest="line_checking_stats", help=argparse.SUPPRESS
    )
    # --debug-cache will disable any cache-related compressions/optimizations,
    # which will make the cache writing process output pretty-printed JSON (which
    # is easier to debug).
    parser.add_argument("--debug-cache", action="store_true", help=argparse.SUPPRESS)
    # --dump-deps will dump all fine-grained dependencies to stdout
    parser.add_argument("--dump-deps", action="store_true", help=argparse.SUPPRESS)
    # --dump-graph will dump the contents of the graph of SCCs and exit.
    parser.add_argument("--dump-graph", action="store_true", help=argparse.SUPPRESS)
    # --semantic-analysis-only does exactly that.
    parser.add_argument("--semantic-analysis-only", action="store_true", help=argparse.SUPPRESS)
    # Some tests use this to tell mypy that we are running a test.
    parser.add_argument("--test-env", action="store_true", help=argparse.SUPPRESS)
    # --local-partial-types disallows partial types spanning module top level and a function
    # (implicitly defined in fine-grained incremental mode)
    add_invertible_flag(
        "--no-local-partial-types",
        inverse="--local-partial-types",
        default=True,
        dest="local_partial_types",
        help=argparse.SUPPRESS,
    )
    # --native-parser enables the native parser (experimental)
    add_invertible_flag(
        "--native-parser",
        default=False,
        help="Enable faster parser that parses directly to mypy AST",
    )
    # --logical-deps adds some more dependencies that are not semantically needed, but
    # may be helpful to determine relative importance of classes and functions for overall
    # type precision in a code base. It also _removes_ some deps, so this flag should be never
    # used except for generating code stats. This also automatically enables --cache-fine-grained.
    # NOTE: This is an experimental option that may be modified or removed at any time.
    parser.add_argument("--logical-deps", action="store_true", help=argparse.SUPPRESS)
    # --bazel changes some behaviors for use with Bazel (https://bazel.build).
    parser.add_argument("--bazel", action="store_true", help=argparse.SUPPRESS)
    # --package-root adds a directory below which directories are considered
    # packages even without __init__.py.  May be repeated.
    parser.add_argument(
        "--package-root", metavar="ROOT", action="append", default=[], help=argparse.SUPPRESS
    )
    # --cache-map FILE ... gives a mapping from source files to cache files.
    # Each triple of arguments is a source file, a cache meta file, and a cache data file.
    # Modules not mentioned in the file will go through cache_dir.
    # Must be followed by another flag or by '--' (and then only file args may follow).
    parser.add_argument(
        "--cache-map", nargs="+", dest="special-opts:cache_map", help=argparse.SUPPRESS
    )
    # --debug-serialize will run tree.serialize() even if cache generation is disabled.
    # Useful for mypy_primer to detect serialize errors earlier.
    parser.add_argument("--debug-serialize", action="store_true", help=argparse.SUPPRESS)

    parser.add_argument(
        "--disable-bytearray-promotion", action="store_true", help=argparse.SUPPRESS
    )
    parser.add_argument(
        "--disable-memoryview-promotion", action="store_true", help=argparse.SUPPRESS
    )
    # This flag is deprecated, it has been moved to --extra-checks
    parser.add_argument("--strict-concatenate", action="store_true", help=argparse.SUPPRESS)

    # options specifying code to check
    code_group = parser.add_argument_group(
        title="Running code",
        description="Specify the code you want to type check. For more details, see "
        "https://mypy.readthedocs.io/en/stable/running_mypy.html#running-mypy",
    )
    add_invertible_flag(
        "--explicit-package-bases",
        default=False,
        help="Use current directory and MYPYPATH to determine module names of files passed",
        group=code_group,
    )
    add_invertible_flag(
        "--fast-module-lookup", default=False, help=argparse.SUPPRESS, group=code_group
    )
    code_group.add_argument(
        "--exclude",
        action="append",
        metavar="PATTERN",
        default=[],
        help=(
            "Regular expression to match file names, directory names or paths which mypy should "
            "ignore while recursively discovering files to check, e.g. --exclude '/setup\\.py$'. "
            "May be specified more than once, eg. --exclude a --exclude b"
        ),
    )
    add_invertible_flag(
        "--exclude-gitignore",
        default=False,
        help=(
            "Use .gitignore file(s) to exclude files from checking "
            "(in addition to any explicit --exclude if present)"
        ),
        group=code_group,
    )
    code_group.add_argument(
        "-m",
        "--module",
        action="append",
        metavar="MODULE",
        default=[],
        dest="special-opts:modules",
        help="Type-check module; can repeat for more modules",
    )
    code_group.add_argument(
        "-p",
        "--package",
        action="append",
        metavar="PACKAGE",
        default=[],
        dest="special-opts:packages",
        help="Type-check package recursively; can be repeated",
    )
    code_group.add_argument(
        "-c",
        "--command",
        action="append",
        metavar="PROGRAM_TEXT",
        dest="special-opts:command",
        help="Type-check program passed in as string",
    )
    code_group.add_argument(
        metavar="files",
        nargs="*",
        dest="special-opts:files",
        help="Type-check given files or directories",
    )
    return parser, strict_flag_names, strict_flag_assignments

