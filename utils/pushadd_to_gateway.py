from typing import Any, Callable, Dict, Optional

def pushadd_to_gateway(
        gateway: str,
        job: str,
        registry: Optional[Collector],
        grouping_key: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = 30,
        handler: Callable = default_handler,
        compression: CompressionType = None,
) -> None:
    """PushAdd metrics to the given pushgateway.

    `gateway` the url for your push gateway. Either of the form
              'http://pushgateway.local', or 'pushgateway.local'.
              Scheme defaults to 'http' if none is provided
    `job` is the job label to be attached to all pushed metrics
    `registry` is a Collector, normally an instance of CollectorRegistry
    `grouping_key` please see the pushgateway documentation for details.
                   Defaults to None
    `timeout` is how long push will attempt to connect before giving up.
              Defaults to 30s, can be set to None for no timeout.
    `handler` is an optional function which can be provided to perform
              requests to the 'gateway'.
              Defaults to None, in which case an http or https request
              will be carried out by a default handler.
              See the 'prometheus_client.push_to_gateway' documentation
              for implementation requirements.
    `compression` selects the payload compression. Supported values are 'gzip'
                  and 'snappy'. Defaults to None (no compression).

    This replaces metrics with the same name, job and grouping_key.
    This uses the POST HTTP method."""
    _use_gateway('POST', gateway, job, registry, grouping_key, timeout, handler, compression)

