
def make_node(action, player=0, prior=1, **kwargs):
  node = async_mcts.SearchNode(action, player, prior)
  for k, v in kwargs.items():
    setattr(node, k, v)
  return node


def make_node(action, player=0, prior=1, **kwargs):
  node = mcts.SearchNode(action, player, prior)
  for k, v in kwargs.items():
    setattr(node, k, v)
  return node

