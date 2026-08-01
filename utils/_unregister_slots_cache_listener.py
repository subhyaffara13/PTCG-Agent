
def _unregister_slots_cache_listener(
    dispatcher_ref: "weakref.ref[EventDispatcher]",
    listener: EventListenerInterface,
    event_type: Type[object],
) -> None:
    # Module-level finalizer callback. Kept free of strong references to the
    # owning ClusterPubSub so attaching it via weakref.finalize does not
    # extend the pubsub's lifetime.
    dispatcher = dispatcher_ref()
    if dispatcher is not None:
        dispatcher.unregister_listeners({event_type: [listener]})


def _unregister_slots_cache_listener(
    dispatcher_ref: "weakref.ref[EventDispatcher]",
    listener: AsyncEventListenerInterface,
    event_type: Type[object],
) -> None:
    # Module-level finalizer callback. Kept free of strong references to the
    # owning ClusterPubSub so attaching it via weakref.finalize does not
    # extend the pubsub's lifetime.
    dispatcher = dispatcher_ref()
    if dispatcher is not None:
        dispatcher.unregister_listeners({event_type: [listener]})

