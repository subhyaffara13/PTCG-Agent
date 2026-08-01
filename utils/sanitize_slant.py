
def sanitizeSlant(userTriple, designTriple, pins, measurements):
    """Sanitize the slant axis limits."""

    log.info("Original slant axis limits: %g:%g:%g", *userTriple)
    log.info(
        "Calculated slant axis limits: %g:%g:%g",
        measurements[designTriple[0]],
        measurements[designTriple[1]],
        measurements[designTriple[2]],
    )

    if (
        abs(measurements[designTriple[0]] - userTriple[0]) > 1
        or abs(measurements[designTriple[1]] - userTriple[1]) > 1
        or abs(measurements[designTriple[2]] - userTriple[2]) > 1
    ):
        log.warning("Calculated slant axis min/default/max do not match user input.")
        log.warning(
            "  Current slant axis limits: %g:%g:%g",
            *userTriple,
        )
        log.warning(
            "  Suggested slant axis limits: %g:%g:%g",
            measurements[designTriple[0]],
            measurements[designTriple[1]],
            measurements[designTriple[2]],
        )

        return False

    return True

