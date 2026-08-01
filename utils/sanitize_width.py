
def sanitizeWidth(userTriple, designTriple, pins, measurements):
    """Sanitize the width axis limits."""

    minVal, defaultVal, maxVal = (
        measurements[designTriple[0]],
        measurements[designTriple[1]],
        measurements[designTriple[2]],
    )

    calculatedMinVal = userTriple[1] * (minVal / defaultVal)
    calculatedMaxVal = userTriple[1] * (maxVal / defaultVal)

    log.info("Original width axis limits: %g:%g:%g", *userTriple)
    log.info(
        "Calculated width axis limits: %g:%g:%g",
        calculatedMinVal,
        userTriple[1],
        calculatedMaxVal,
    )

    if (
        abs(calculatedMinVal - userTriple[0]) / userTriple[1] > 0.05
        or abs(calculatedMaxVal - userTriple[2]) / userTriple[1] > 0.05
    ):
        log.warning("Calculated width axis min/max do not match user input.")
        log.warning(
            "  Current width axis limits: %g:%g:%g",
            *userTriple,
        )
        log.warning(
            "  Suggested width axis limits: %g:%g:%g",
            calculatedMinVal,
            userTriple[1],
            calculatedMaxVal,
        )

        return False

    return True

