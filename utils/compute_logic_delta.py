
def compute_logic_delta(logs):
    reasoning_logs = logs["reasoning_test"]["reasoning"] or []
    fired = [log for log in reasoning_logs if log.get("reasoning_fired") is True]
    if not fired:
        return 0.0
    return (sum(1 for log in fired if log.get("reasoning_outcome") == "positive") -
            sum(1 for log in fired if log.get("reasoning_outcome") == "negative")) / len(fired)

