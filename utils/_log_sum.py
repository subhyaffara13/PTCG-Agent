
def _log_sum(log_p, log_q):
    return sc.logsumexp([log_p, log_q], axis=0)

