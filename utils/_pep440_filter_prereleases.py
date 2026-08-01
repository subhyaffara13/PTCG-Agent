
def _pep440_filter_prereleases(
    iterable: Iterable[Any], key: Callable[[Any], UnparsedVersion] | None
) -> Iterator[Any]:
    """Filter per PEP 440: exclude prereleases unless no finals exist."""
    # Two lists used:
    #   * all_nonfinal to preserve order if no finals exist
    #   * arbitrary_strings for streaming when first final found
    all_nonfinal: list[Any] = []
    arbitrary_strings: list[Any] = []

    found_final = False
    for item in iterable:
        parsed = _coerce_version(item if key is None else key(item))

        if parsed is None:
            # Arbitrary strings are always included as it is not
            # possible to determine if they are prereleases,
            # and they have already passed all specifiers.
            if found_final:
                yield item
            else:
                arbitrary_strings.append(item)
                all_nonfinal.append(item)
            continue

        if not parsed.is_prerelease:
            # Final release found - flush arbitrary strings, then yield
            if not found_final:
                yield from arbitrary_strings
                found_final = True
            yield item
            continue

        # Prerelease - buffer if no finals yet, otherwise skip
        if not found_final:
            all_nonfinal.append(item)

    # No finals found - yield all buffered items
    if not found_final:
        yield from all_nonfinal


def _pep440_filter_prereleases(
    iterable: Iterable[Any], key: Callable[[Any], UnparsedVersion] | None
) -> Iterator[Any]:
    """Filter per PEP 440: exclude prereleases unless no finals exist."""
    # Two lists used:
    #   * all_nonfinal to preserve order if no finals exist
    #   * arbitrary_strings for streaming when first final found
    all_nonfinal: list[Any] = []
    arbitrary_strings: list[Any] = []

    found_final = False
    for item in iterable:
        parsed = _coerce_version(item if key is None else key(item))

        if parsed is None:
            # Arbitrary strings are always included as it is not
            # possible to determine if they are prereleases,
            # and they have already passed all specifiers.
            if found_final:
                yield item
            else:
                arbitrary_strings.append(item)
                all_nonfinal.append(item)
            continue

        if not parsed.is_prerelease:
            # Final release found - flush arbitrary strings, then yield
            if not found_final:
                yield from arbitrary_strings
                found_final = True
            yield item
            continue

        # Prerelease - buffer if no finals yet, otherwise skip
        if not found_final:
            all_nonfinal.append(item)

    # No finals found - yield all buffered items
    if not found_final:
        yield from all_nonfinal

