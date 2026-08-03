import logging

def wait_for_signals(
    receive_signals: Sequence[synchronization.HandlerAwaitableSignal],
    *,
    timeout_secs: int,
    operation_id: str,
):
  """Waits for signals to be set."""
  for signal in receive_signals:
    logging.vlog(
        1,
        '[process=%d][thread=%s][operation_id=%s] Waiting for <%s> timeout:'
        ' %d secs to be set',
        multihost.process_index(),
        threading.current_thread().name,
        operation_id,
        signal.value,
        timeout_secs,
    )
    barrier_key = AwaitableSignalsContract.get_unique_awaitable_singal_key(
        signal, operation_id
    )
    client = signaling_client.get_signaling_client()
    client.blocking_key_value_get(barrier_key, timeout_secs)

