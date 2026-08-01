
def _get_message(warn_info):
    return next(warn.message.args[0] for warn in warn_info)


def _get_message(status):
    """
    Given problem status code, return a more detailed message.

    Parameters
    ----------
    status : int
        An integer representing the exit status of the optimization::

         0 : Optimization terminated successfully
         1 : Iteration limit reached
         2 : Problem appears to be infeasible
         3 : Problem appears to be unbounded
         4 : Serious numerical difficulties encountered

    Returns
    -------
    message : str
        A string descriptor of the exit status of the optimization.

    """
    messages = (
        ["Optimization terminated successfully.",
         "The iteration limit was reached before the algorithm converged.",
         "The algorithm terminated successfully and determined that the "
         "problem is infeasible.",
         "The algorithm terminated successfully and determined that the "
         "problem is unbounded.",
         "Numerical difficulties were encountered before the problem "
         "converged. Please check your problem formulation for errors, "
         "independence of linear equality constraints, and reasonable "
         "scaling and matrix condition numbers. If you continue to "
         "encounter this error, please submit a bug report."
         ])
    return messages[status]

