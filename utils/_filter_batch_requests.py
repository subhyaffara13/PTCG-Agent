
def _filter_batch_requests(
    batch_requests: BatchRequests,
    additions: Set[Any],
) -> BatchRequests:
  """Filters batch requests to include only items matching the additions."""
  filtered_requests = []
  for request in batch_requests:
    filtered_items = []
    for key, value, info, arg in zip(
        request.keys, request.values, request.infos, request.args
    ):
      for add in additions:
        # Additions may be a prefix/parent of the key.
        if add == key[: len(add)]:
          filtered_items.append((key, value, info, arg))
    if filtered_items:
      keys, values, infos, args = zip(*filtered_items)
      filtered_requests.append(
          dataclasses.replace(
              request,
              keys=list(keys),
              values=list(values),
              infos=list(infos),
              args=list(args),
          )
      )
  return filtered_requests

