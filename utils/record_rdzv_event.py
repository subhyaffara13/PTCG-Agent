
def record_rdzv_event(event: RdzvEvent) -> None:
    _get_or_create_logger("dynamic_rendezvous").info(event.serialize())

