
def print_results(
    hits: list[TransformedHit],
    name_column_width: int | None = None,
    terminal_width: int | None = None,
) -> None:
    if not hits:
        return
    if name_column_width is None:
        name_column_width = (
            max(
                [
                    len(hit["name"]) + len(highest_version(hit.get("versions", ["-"])))
                    for hit in hits
                ]
            )
            + 4
        )

    for hit in hits:
        name = hit["name"]
        summary = hit["summary"] or ""
        latest = highest_version(hit.get("versions", ["-"]))
        if terminal_width is not None:
            target_width = terminal_width - name_column_width - 5
            if target_width > 10:
                # wrap and indent summary to fit terminal
                summary_lines = textwrap.wrap(summary, target_width)
                summary = ("\n" + " " * (name_column_width + 3)).join(summary_lines)

        name_latest = f"{name} ({latest})"
        line = f"{name_latest:{name_column_width}} - {summary}"
        try:
            write_output(line)
            dist = get_installed_distribution(name)
            print_dist_installation_info(latest, dist)
        except UnicodeEncodeError:
            pass


def print_results(
    distributions: Iterable[_PackageInfo],
    list_files: bool,
    verbose: bool,
) -> bool:
    """
    Print the information from installed distributions found.
    """
    results_printed = False
    for i, dist in enumerate(distributions):
        results_printed = True
        if i > 0:
            write_output("---")

        metadata_version_tuple = tuple(map(int, dist.metadata_version.split(".")))

        write_output("Name: %s", dist.name)
        write_output("Version: %s", dist.version)
        write_output("Summary: %s", dist.summary)
        write_output("Home-page: %s", dist.homepage)
        write_output("Author: %s", dist.author)
        write_output("Author-email: %s", dist.author_email)
        if metadata_version_tuple >= (2, 4) and dist.license_expression:
            write_output("License-Expression: %s", dist.license_expression)
        else:
            write_output("License: %s", dist.license)
        write_output("Location: %s", dist.location)
        if dist.editable_project_location is not None:
            write_output(
                "Editable project location: %s", dist.editable_project_location
            )
        write_output("Requires: %s", ", ".join(dist.requires))
        write_output("Required-by: %s", ", ".join(dist.required_by))

        if verbose:
            write_output("Metadata-Version: %s", dist.metadata_version)
            write_output("Installer: %s", dist.installer)
            write_output("Classifiers:")
            for classifier in dist.classifiers:
                write_output("  %s", classifier)
            write_output("Entry-points:")
            for entry in dist.entry_points:
                write_output("  %s", entry.strip())
            write_output("Project-URLs:")
            for project_url in dist.project_urls:
                write_output("  %s", project_url)
        if list_files:
            write_output("Files:")
            if dist.files is None:
                write_output("Cannot locate RECORD or installed-files.txt")
            else:
                for line in dist.files:
                    write_output("  %s", line.strip())
    return results_printed


def print_results(payoff_tables,
                  payoffs_are_hpt_format,
                  rhos=None,
                  rho_m=None,
                  c=None,
                  pi=None):
  """Prints the finite-population analysis results."""

  print('Payoff tables:\n')
  if payoffs_are_hpt_format:
    for payoff_table in payoff_tables:
      print(payoff_table())
  else:
    print(payoff_tables)
  if rho_m is not None:
    print('\nNeutral fixation probability (rho_m):\n', rho_m)
  if rhos is not None and rho_m is not None:
    print('\nFixation probability matrix (rho_{r,s}/rho_m):\n',
          np.around(rhos / rho_m, decimals=2))
  if c is not None:
    print('\nMarkov transition matrix (c):\n', np.around(c, decimals=2))
  if pi is not None:
    print('\nStationary distribution (pi):\n', pi)

