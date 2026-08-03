from pathlib import Path


def test_doc_pyplot_summary():
    """Test that pyplot_summary lists all the plot functions."""
    pyplot_docs = Path(__file__).parent / '../../../doc/api/pyplot_summary.rst'
    if not pyplot_docs.exists():
        pytest.skip("Documentation sources not available")

    def extract_documented_functions(lines):
        """
        Return a list of all the functions that are mentioned in the
        autosummary blocks contained in *lines*.

        An autosummary block looks like this::

            .. autosummary::
               :toctree: _as_gen
               :template: autosummary.rst
               :nosignatures:

               plot
               errorbar

        """
        functions = []
        in_autosummary = False
        for line in lines:
            if not in_autosummary:
                if line.startswith(".. autosummary::"):
                    in_autosummary = True
            else:
                if not line or line.startswith("   :"):
                    # empty line or autosummary parameter
                    continue
                if not line[0].isspace():
                    # no more indentation: end of autosummary block
                    in_autosummary = False
                    continue
                functions.append(line.strip())
        return functions

    lines = pyplot_docs.read_text().split("\n")
    doc_functions = set(extract_documented_functions(lines))
    plot_commands = set(plt._get_pyplot_commands())
    missing = plot_commands.difference(doc_functions)
    if missing:
        raise AssertionError(
            f"The following pyplot functions are not listed in the "
            f"documentation. Please add them to doc/api/pyplot_summary.rst: "
            f"{missing!r}")
    extra = doc_functions.difference(plot_commands)
    if extra:
        raise AssertionError(
            f"The following functions are listed in the pyplot documentation, "
            f"but they do not exist in pyplot. "
            f"Please remove them from doc/api/pyplot_summary.rst: {extra!r}")

