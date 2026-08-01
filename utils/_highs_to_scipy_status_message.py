
def _highs_to_scipy_status_message(highs_status, highs_message):
    """Converts HiGHS status number/message to SciPy status number/message"""

    scipy_statuses_messages = {
        None: (4, "HiGHS did not provide a status code. "),
        HighsModelStatus.kNotset: (4, ""),
        HighsModelStatus.kLoadError: (4, ""),
        HighsModelStatus.kModelError: (2, ""),
        HighsModelStatus.kPresolveError: (4, ""),
        HighsModelStatus.kSolveError: (4, ""),
        HighsModelStatus.kPostsolveError: (4, ""),
        HighsModelStatus.kModelEmpty: (4, ""),
        HighsModelStatus.kObjectiveBound: (4, ""),
        HighsModelStatus.kObjectiveTarget: (4, ""),
        HighsModelStatus.kOptimal: (0, "Optimization terminated successfully. "),
        HighsModelStatus.kTimeLimit: (1, "Time limit reached. "),
        HighsModelStatus.kIterationLimit: (1, "Iteration limit reached. "),
        HighsModelStatus.kInfeasible: (2, "The problem is infeasible. "),
        HighsModelStatus.kUnbounded: (3, "The problem is unbounded. "),
        HighsModelStatus.kUnboundedOrInfeasible: (4, "The problem is unbounded "
                                                  "or infeasible. ")}
    unrecognized = (4, "The HiGHS status code was not recognized. ")
    scipy_status, scipy_message = (
        scipy_statuses_messages.get(highs_status, unrecognized))
    hstat = int(highs_status) if highs_status is not None else None
    scipy_message = (f"{scipy_message}"
                     f"(HiGHS Status {hstat}: {highs_message})")
    return scipy_status, scipy_message

