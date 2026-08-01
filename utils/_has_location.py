
def _has_location(
    request: (
        tiering_service_pb2.ReserveRequest | tiering_service_pb2.PrefetchRequest
    ),
) -> bool:
  """Checks whether request specifies a location (zone or region)."""
  return bool(request.zone or request.region)

