import sys

def audit() -> None:  # pragma: no cover
    """
    The primary entrypoint for `pip-audit`.
    """
    parser = _parser()
    args = _parse_args(parser)

    service: VulnerabilityService
    if args.vulnerability_service is VulnerabilityServiceChoice.Osv:
        service = OsvService(cache_dir=args.cache_dir, timeout=args.timeout, osv_url=args.osv_url)
    elif args.vulnerability_service is VulnerabilityServiceChoice.Pypi:
        service = PyPIService(cache_dir=args.cache_dir, timeout=args.timeout)
    elif args.vulnerability_service is VulnerabilityServiceChoice.Esms:
        service = EcosystemsService(cache_dir=args.cache_dir, timeout=args.timeout)
    else:
        assert_never(args.vulnerability_service)  # pragma: no cover

    output_desc = args.desc.to_bool(args.format)
    output_aliases = args.aliases.to_bool(args.format)
    formatter = args.format.to_format(output_desc, output_aliases)

    # Check for flags that are only valid with project paths
    if args.project_path is None:
        if args.locked:
            parser.error("The --locked flag can only be used with a project path")

    # Check for flags that are only valid with requirements files
    if args.requirements is None:
        if args.require_hashes:
            parser.error("The --require-hashes flag can only be used with --requirement (-r)")
        elif args.index_url:
            parser.error("The --index-url flag can only be used with --requirement (-r)")
        elif args.extra_index_urls:
            parser.error("The --extra-index-url flag can only be used with --requirement (-r)")
        elif args.no_deps:
            parser.error("The --no-deps flag can only be used with --requirement (-r)")
        elif args.disable_pip:
            parser.error("The --disable-pip flag can only be used with --requirement (-r)")

    # Nudge users to consider alternate workflows.
    if args.require_hashes and args.no_deps:
        logger.warning("The --no-deps flag is redundant when used with --require-hashes")

    if args.require_hashes and isinstance(service, OsvService):
        logger.warning(
            "The --require-hashes flag with --service osv only enforces hash presence NOT hash "
            "validity. Use --service pypi to enforce hash validity."
        )

    if args.no_deps:
        logger.warning(
            "--no-deps is supported, but users are encouraged to fully hash their "
            "pinned dependencies"
        )
        logger.warning(
            "Consider using a tool like `pip-compile`: "
            "https://pip-tools.readthedocs.io/en/latest/#using-hashes"
        )

    with ExitStack() as stack:
        actors = []
        if args.progress_spinner:
            actors.append(AuditSpinner("Collecting inputs"))
        state = stack.enter_context(AuditState(members=actors))

        source: DependencySource
        if args.requirements is not None:
            for req in args.requirements:
                if not req.exists():
                    _fatal(f"invalid requirements input: {req}")

            source = RequirementSource(
                args.requirements,
                require_hashes=args.require_hashes,
                no_deps=args.no_deps,
                disable_pip=args.disable_pip,
                skip_editable=args.skip_editable,
                index_url=args.index_url,
                extra_index_urls=args.extra_index_urls,
                state=state,
            )
        elif args.project_path is not None:
            # NOTE: We'll probably want to support --skip-editable here,
            # once PEP 660 is more widely supported: https://www.python.org/dev/peps/pep-0660/

            # Determine which kind of project file exists in the project path
            source = _dep_source_from_project_path(
                args.project_path,
                args.index_url,
                args.extra_index_urls,
                args.locked,
                state,
            )
        else:
            source = PipSource(
                local=args.local,
                paths=args.paths,
                skip_editable=args.skip_editable,
                state=state,
            )

        # `--dry-run` only affects the auditor if `--fix` is also not supplied,
        # since the combination of `--dry-run` and `--fix` implies that the user
        # wants to dry-run the "fix" step instead of the "audit" step
        auditor = Auditor(service, options=AuditOptions(dry_run=args.dry_run and not args.fix))

        result: dict[Dependency, list[VulnerabilityResult]] = {}
        pkg_count = 0
        vuln_count = 0
        skip_count = 0
        vuln_ignore_count = 0
        vulns_to_ignore = set(args.ignore_vulns)
        try:
            for spec, vulns in auditor.audit(source):
                if spec.is_skipped():
                    spec = cast(SkippedDependency, spec)
                    if args.strict:
                        _fatal(f"{spec.name}: {spec.skip_reason}")
                    else:
                        state.update_state(f"Skipping {spec.name}: {spec.skip_reason}")
                    skip_count += 1
                else:
                    spec = cast(ResolvedDependency, spec)
                    logger.debug(f"Auditing {spec.name} ({spec.version})")
                    state.update_state(f"Auditing {spec.name} ({spec.version})")
                if vulns_to_ignore:
                    filtered_vulns = [v for v in vulns if not v.has_any_id(vulns_to_ignore)]
                    vuln_ignore_count += len(vulns) - len(filtered_vulns)
                    vulns = filtered_vulns
                result[spec] = vulns
                if len(vulns) > 0:
                    pkg_count += 1
                    vuln_count += len(vulns)
        except DependencySourceError as e:
            _fatal(str(e))
        except VulnServiceConnectionError as e:
            # The most common source of connection errors is corporate blocking,
            # so we offer a bit of advice.
            logger.error(str(e))
            _fatal(
                "Tip: your network may be blocking this service. "
                "Try another service with `-s SERVICE`"
            )

        # If the `--fix` flag has been applied, find a set of suitable fix versions and upgrade the
        # dependencies at the source
        fixes = []
        fixed_pkg_count = 0
        fixed_vuln_count = 0
        if args.fix:
            for fix in resolve_fix_versions(service, result, state):
                if args.dry_run:
                    if fix.is_skipped():
                        fix = cast(SkippedFixVersion, fix)
                        logger.info(
                            f"Dry run: would have skipped {fix.dep.name} "
                            f"upgrade because {fix.skip_reason}"
                        )
                    else:
                        fix = cast(ResolvedFixVersion, fix)
                        logger.info(f"Dry run: would have upgraded {fix.dep.name} to {fix.version}")
                    continue

                if not fix.is_skipped():
                    fix = cast(ResolvedFixVersion, fix)
                    try:
                        source.fix(fix)
                        fixed_pkg_count += 1
                        fixed_vuln_count += len(result[fix.dep])
                    except DependencySourceError as dse:
                        skip_reason = str(dse)
                        logger.debug(skip_reason)
                        fix = SkippedFixVersion(fix.dep, skip_reason)
                fixes.append(fix)

    if vuln_count > 0:
        if vuln_ignore_count:
            ignored = f", ignored {vuln_ignore_count}"
        else:
            ignored = ""

        summary_msg = (
            f"Found {vuln_count} known "
            f"{'vulnerability' if vuln_count == 1 else 'vulnerabilities'}"
            f"{ignored} in {pkg_count} {'package' if pkg_count == 1 else 'packages'}"
        )
        if args.fix:
            summary_msg += (
                f" and fixed {fixed_vuln_count} "
                f"{'vulnerability' if fixed_vuln_count == 1 else 'vulnerabilities'} "
                f"in {fixed_pkg_count} "
                f"{'package' if fixed_pkg_count == 1 else 'packages'}"
            )
        print(summary_msg, file=sys.stderr)
        with _output_io(args.output) as io:
            print(formatter.format(result, fixes), file=io)
        if pkg_count != fixed_pkg_count:
            sys.exit(1)
    else:
        summary_msg = "No known vulnerabilities found"
        if vuln_ignore_count:
            summary_msg += f", {vuln_ignore_count} ignored"

        print(
            summary_msg,
            file=sys.stderr,
        )
        # If our output format is a "manifest" format we always emit it,
        # even if nothing other than a dependency summary is present.
        if skip_count > 0 or formatter.is_manifest:
            with _output_io(args.output) as io:
                print(formatter.format(result, fixes), file=io)

