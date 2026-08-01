
def _check_format_errors_warnings(routine_name, err_lst):
    # XXX: find a test case to cover this
    mesg = (
        f"Internal {routine_name} return info = {[e['lapack_info'] for e in err_lst]} "
        f"for slices {[e['num'] for e in err_lst]}."
    )
    raise LinAlgError(mesg)


def _check_format_errors_warnings(routine_name, err_lst):
    msg = (
        f"Internal {routine_name} return info = {[e['lapack_info'] for e in err_lst]} "
        f"for slices {[e['num'] for e in err_lst]}."
    )
    raise LinAlgError(msg)

