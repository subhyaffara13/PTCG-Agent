
def multiproc(request):
    """
    Return True if running under xdist and multiple
    workers are used.
    """
    try:
        worker_id = request.getfixturevalue('worker_id')
    except Exception:
        return False
    return worker_id != 'master'

