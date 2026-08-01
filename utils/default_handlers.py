
def default_handlers() -> list[DebugHandler]:
    return [
        IndexHandler(),
        StacksHandler(),
        PySpyHandler(),
        FlightRecorderHandler(),
        TorchCommsFlightRecorderHandler(),
        ProfilerHandler(),
        WaitCountersHandler(),
        TCPStoreHandler(),
    ]

