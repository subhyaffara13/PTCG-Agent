
def _new_deal(controller, seat, hand, board):
  """Informs a BlueChip bots that there is a new deal."""
  controller.send_line(_START_BOARD)
  _expect(controller, _READY_FOR_DEAL.format(seat=seat))
  controller.send_line(_DEAL.format(board=board))
  _expect(controller, _READY_FOR_CARDS.format(seat=seat))
  controller.send_line(_CARDS.format(seat=seat, hand=hand))

