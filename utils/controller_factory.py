
def controller_factory():
  """Implements bluechip_bridge.BlueChipBridgeBot."""
  client = _WBridge5Client(FLAGS.bot_cmd)
  client.start()
  return client

