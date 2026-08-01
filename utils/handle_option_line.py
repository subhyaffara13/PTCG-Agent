
def handle_option_line(opts: Values) -> Dict:
    """
    Return a mapping of {name: value} for supported pip options.
    """
    options = {}
    for name in SUPPORTED_OPTIONS_DEST + LEGACY_OPTIONS_DEST:
        if hasattr(opts, name):
            value = getattr(opts, name)
            if name in options:
                # An option cannot be repeated on a single line
                raise InstallationError(f"Invalid duplicated option name: {name}")
            if value:
                # strip possible legacy leading equal
                if isinstance(value, str):
                    value = value.lstrip("=")
                if isinstance(value, list):
                    value = [v.lstrip("=") for v in value]
                options[name] = value

    return options


def handle_option_line(
    opts: Values,
    filename: str,
    lineno: int,
    finder: PackageFinder | None = None,
    options: optparse.Values | None = None,
    session: PipSession | None = None,
) -> None:
    if opts.hashes:
        logger.warning(
            "%s line %s has --hash but no requirement, and will be ignored.",
            filename,
            lineno,
        )

    if options:
        # percolate options upward
        if opts.require_hashes:
            options.require_hashes = opts.require_hashes
        if opts.features_enabled:
            options.features_enabled.extend(
                f for f in opts.features_enabled if f not in options.features_enabled
            )

    # set finder options
    if finder:
        find_links = finder.find_links
        index_urls = finder.index_urls
        no_index = finder.search_scope.no_index
        if opts.no_index is True:
            no_index = True
            index_urls = []
        if opts.index_url and not no_index:
            index_urls = [opts.index_url]
        if opts.extra_index_urls and not no_index:
            index_urls.extend(opts.extra_index_urls)
        if opts.find_links:
            # FIXME: it would be nice to keep track of the source
            # of the find_links: support a find-links local path
            # relative to a requirements file.
            value = opts.find_links[0]
            req_dir = os.path.dirname(os.path.abspath(filename))
            relative_to_reqs_file = os.path.join(req_dir, value)
            if os.path.exists(relative_to_reqs_file):
                value = relative_to_reqs_file
            find_links.append(value)

        if session:
            # We need to update the auth urls in session
            session.update_index_urls(index_urls)

        search_scope = SearchScope(
            find_links=find_links,
            index_urls=index_urls,
            no_index=no_index,
        )
        finder.search_scope = search_scope

        # Transform --pre into --all-releases :all:
        if opts.pre:
            if not opts.release_control:
                opts.release_control = ReleaseControl()
            opts.release_control.all_releases.add(":all:")

        if opts.release_control:
            if not finder.release_control:
                # First time seeing release_control, set it on finder
                finder.set_release_control(opts.release_control)

        if opts.prefer_binary:
            finder.set_prefer_binary()

        if session:
            for host in opts.trusted_hosts or []:
                source = f"line {lineno} of {filename}"
                session.add_trusted_host(host, source=source)

