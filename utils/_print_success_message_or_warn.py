
def _print_success_message_or_warn(warnflag, message, warntype=None):
    if not warnflag:
        print(message)
    else:
        warnings.warn(message, warntype or OptimizeWarning, stacklevel=3)

