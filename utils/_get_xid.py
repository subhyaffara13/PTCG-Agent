
def _get_xid() -> int:
  """Returns the XID for this run."""
  xid = multihost_utils.broadcast_one_to_all(
      np.asarray(int(time.time()))
  ).item()
  logging.info("XID: %s", xid)
  return xid

