
def _connect(controller, seat):
  """Performs the initial handshake with a BlueChip bot."""
  client_name = _expect_regex(controller, _CONNECT)["client_name"]
  controller.send_line(_SEATED.format(seat=seat, client_name=client_name))
  _expect(controller, _READY_FOR_TEAMS.format(seat=seat))
  controller.send_line(_TEAMS)
  _expect(controller, _READY_TO_START.format(seat=seat))


def _connect(client, seat, state_vec):
  """Performs the initial handshake with a BlueChip bot."""
  client.start()
  client_name = _expect_regex(client, _CONNECT)["client_name"]
  client.send_line(_SEATED.format(seat=seat, client_name=client_name))
  _expect(client, _READY_FOR_TEAMS.format(seat=seat))
  client.send_line(_TEAMS)
  _expect(client, _READY_TO_START.format(seat=seat))
  client.send_line(_START_BOARD)
  _expect(client, _READY_FOR_DEAL.format(seat=seat))
  client.send_line(_DEAL)
  _expect(client, _READY_FOR_CARDS.format(seat=seat))
  client.send_line(_CARDS.format(seat=seat, hand=_hand_string(state_vec)))

