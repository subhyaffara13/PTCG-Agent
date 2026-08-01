
def parse_pubsub_subscriptions(
    args: tuple[Any, ...], kwargs: Mapping[str, PubSubHandler]
) -> dict[ChannelT, PubSubHandler | None]:
    parsed_args = list_or_args(args[0], args[1:]) if args else []
    subscriptions: dict[ChannelT, PubSubHandler | None] = {}
    for arg in parsed_args:
        if isinstance(arg, Subscription):
            subscriptions[arg.name] = arg.handler
        else:
            subscriptions[arg] = None
    subscriptions.update(kwargs)
    return subscriptions

