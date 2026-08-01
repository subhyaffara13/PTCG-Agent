
def raise_if_quarto_is_not_available(min_version=QUARTO_MIN_VERSION):
    """Raise with an informative error message if quarto is not available"""
    version = quarto_version()
    if version == "N/A":
        raise QuartoError(f"The Quarto Markdown format requires 'quarto>={min_version}', but quarto was not found")

    if parse(version) < parse(min_version):
        raise QuartoError(
            f"The Quarto Markdown format requires 'quarto>={min_version}', but quarto version {version} was found"
        )

    return version

