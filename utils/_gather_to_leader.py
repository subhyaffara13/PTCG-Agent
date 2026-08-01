
def _gather_to_leader(sequence_id, worker_name, obj, worker_names=None):
    with _all_gather_dict_lock:
        if not worker_names:
            worker_names = _ALL_WORKER_NAMES
            if worker_name not in worker_names:
                raise AssertionError(f"{worker_name} is not expected by leader.")
        states = _all_gather_sequence_id_to_states[sequence_id]
        if worker_name in states.gathered_objects:
            raise AssertionError(
                f"{worker_name} reported intent sequence id {sequence_id} twice. "
            )
        states.gathered_objects[worker_name] = obj
        if worker_names == set(states.gathered_objects.keys()):
            states.proceed_signal.set()

