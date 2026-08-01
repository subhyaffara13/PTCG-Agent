
def _warn_incompatibility_with_xunit2(
    request: FixtureRequest, fixture_name: str
) -> None:
    """Emit a PytestWarning about the given fixture being incompatible with newer xunit revisions."""
    from _pytest.warning_types import PytestWarning

    xml = request.config.stash.get(xml_key, None)
    if xml is not None and xml.family not in ("xunit1", "legacy"):
        request.node.warn(
            PytestWarning(
                f"{fixture_name} is incompatible with junit_family '{xml.family}' (use 'legacy' or 'xunit1')"
            )
        )

