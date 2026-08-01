
def set_signals(
    send_signals: Sequence[synchronization.HandlerAwaitableSignal],
    *,
    operation_id: str,
):
  """Sets the barrier keys for the signals using send_signals."""
  for signal in send_signals:
    logging.vlog(
        1,
        '[process=%d][thread=%s][operation_id=%s] Signalling completion of'
        ' <%s>.',
        multihost.process_index(),
        threading.current_thread().name,
        operation_id,
        signal.value,
    )
    barrier_key = AwaitableSignalsContract.get_unique_awaitable_singal_key(
        signal, operation_id
    )
    client = signaling_client.get_signaling_client()
    client.key_value_set(
        barrier_key, _SIGNAL_ACTION_SUCCESS, allow_overwrite=True
    )

