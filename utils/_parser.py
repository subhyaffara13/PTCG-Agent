
def _parser() -> argparse.ArgumentParser:  # pragma: no cover
    parser = argparse.ArgumentParser(
        prog="pip-audit",
        description="audit the Python environment for dependencies with known vulnerabilities",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    dep_source_args = parser.add_mutually_exclusive_group()
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "-l",
        "--local",
        action="store_true",
        help="show only results for dependencies in the local environment",
    )
    dep_source_args.add_argument(
        "-r",
        "--requirement",
        type=Path,
        metavar="REQUIREMENT",
        action="append",
        dest="requirements",
        help="audit the given requirements file; this option can be used multiple times",
    )
    dep_source_args.add_argument(
        "project_path",
        type=Path,
        nargs="?",
        help="audit a local Python project at the given path",
    )
    parser.add_argument(
        "--locked",
        action="store_true",
        help="audit lock files from the local Python project. This "
        "flag only applies to auditing from project paths",
    )
    parser.add_argument(
        "-f",
        "--format",
        type=OutputFormatChoice,
        choices=OutputFormatChoice,
        default=os.environ.get("PIP_AUDIT_FORMAT", OutputFormatChoice.Columns),
        metavar="FORMAT",
        help=_enum_help("the format to emit audit results in", OutputFormatChoice),
    )
    parser.add_argument(
        "-s",
        "--vulnerability-service",
        type=VulnerabilityServiceChoice,
        choices=VulnerabilityServiceChoice,
        default=os.environ.get("PIP_AUDIT_VULNERABILITY_SERVICE", VulnerabilityServiceChoice.Pypi),
        metavar="SERVICE",
        help=_enum_help(
            "the vulnerability service to audit dependencies against",
            VulnerabilityServiceChoice,
        ),
    )
    parser.add_argument(
        "--osv-url",
        type=str,
        metavar="OSV_URL",
        dest="osv_url",
        default=os.environ.get("PIP_AUDIT_OSV_URL", OsvService.DEFAULT_OSV_URL),
        help="URL to use for the OSV API instead of the default",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="without `--fix`: collect all dependencies but do not perform the auditing step; "
        "with `--fix`: perform the auditing step but do not perform any fixes",
    )
    parser.add_argument(
        "-S",
        "--strict",
        action="store_true",
        help="fail the entire audit if dependency collection fails on any dependency",
    )
    parser.add_argument(
        "--desc",
        type=VulnerabilityDescriptionChoice,
        choices=VulnerabilityDescriptionChoice,
        nargs="?",
        const=VulnerabilityDescriptionChoice.On,
        default=os.environ.get("PIP_AUDIT_DESC", VulnerabilityDescriptionChoice.Auto),
        help="include a description for each vulnerability; "
        "`auto` defaults to `on` for the `json` format. This flag has no "
        "effect on the `cyclonedx-json` or `cyclonedx-xml` formats.",
    )
    parser.add_argument(
        "--aliases",
        type=VulnerabilityAliasChoice,
        choices=VulnerabilityAliasChoice,
        nargs="?",
        const=VulnerabilityAliasChoice.On,
        default=VulnerabilityAliasChoice.Auto,
        help="includes alias IDs for each vulnerability; "
        "`auto` defaults to `on` for the `json` format. This flag has no "
        "effect on the `cyclonedx-json` or `cyclonedx-xml` formats.",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        help="the directory to use as an HTTP cache for PyPI; uses the `pip` HTTP cache by default",
    )
    parser.add_argument(
        "--progress-spinner",
        type=ProgressSpinnerChoice,
        choices=ProgressSpinnerChoice,
        default=os.environ.get("PIP_AUDIT_PROGRESS_SPINNER", ProgressSpinnerChoice.On),
        help="display a progress spinner",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="set the socket timeout",  # Match the `pip` default
    )
    dep_source_args.add_argument(
        "--path",
        type=Path,
        metavar="PATH",
        action="append",
        dest="paths",
        default=[],
        help="restrict to the specified installation path for auditing packages; "
        "this option can be used multiple times",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="run with additional debug logging; supply multiple times to increase verbosity",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="automatically upgrade dependencies with known vulnerabilities",
    )
    parser.add_argument(
        "--require-hashes",
        action="store_true",
        help="require a hash to check each requirement against, for repeatable audits; this option "
        "is implied when any package in a requirements file has a `--hash` option.",
    )
    parser.add_argument(
        "--index-url",
        type=str,
        help="base URL of the Python Package Index; this should point to a repository compliant "
        "with PEP 503 (the simple repository API); this will be resolved by pip if not specified",
    )
    parser.add_argument(
        "--extra-index-url",
        type=str,
        metavar="URL",
        action="append",
        dest="extra_index_urls",
        default=[],
        help="extra URLs of package indexes to use in addition to `--index-url`; should follow the "
        "same rules as `--index-url`",
    )
    parser.add_argument(
        "--skip-editable",
        action="store_true",
        help="don't audit packages that are marked as editable",
    )
    parser.add_argument(
        "--no-deps",
        action="store_true",
        help="don't perform any dependency resolution; requires all requirements are pinned "
        "to an exact version",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        metavar="FILE",
        help="output results to the given file",
        default=os.environ.get("PIP_AUDIT_OUTPUT", "stdout"),
    )
    parser.add_argument(
        "--ignore-vuln",
        type=str,
        metavar="ID",
        action="append",
        dest="ignore_vulns",
        default=[],
        help=(
            "ignore a specific vulnerability by its vulnerability ID; "
            "this option can be used multiple times"
        ),
    )
    parser.add_argument(
        "--disable-pip",
        action="store_true",
        help="don't use `pip` for dependency resolution; "
        "this can only be used with hashed requirements files or if the `--no-deps` flag has been "
        "provided",
    )
    return parser

