
def _get_current_remote_pip_version(
    session: PipSession, options: optparse.Values
) -> str | None:
    # Lets use PackageFinder to see what the latest pip version is
    link_collector = LinkCollector.create(
        session,
        options=options,
        suppress_no_index=True,
    )

    # Pass allow_yanked=False so we don't suggest upgrading to a
    # yanked version.
    selection_prefs = SelectionPreferences(
        allow_yanked=False,
        release_control=ReleaseControl(only_final={"pip"}),
    )

    finder = PackageFinder.create(
        link_collector=link_collector,
        selection_prefs=selection_prefs,
    )
    best_candidate = finder.find_best_candidate("pip").best_candidate
    if best_candidate is None:
        return None

    return str(best_candidate.version)

