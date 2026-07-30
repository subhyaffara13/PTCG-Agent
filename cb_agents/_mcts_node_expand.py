from cb_agents.value_network import ActionPrior
from cb_agents.mcts_node import MCTSNode

def expand_node(node: MCTSNode, action_priors):
    chance_actions = ["crushing_hammer", "pokemon_catcher", "super_scoop_up", "pokeball"]
    for ap in action_priors:
        if ap.action not in node.children:
            is_chance = any(ca in ap.action.lower() for ca in chance_actions)
            if is_chance:
                chance_node = MCTSNode(
                    state_hash=f"{node.state_hash}_{ap.action}_chance",
                    parent=node, action_taken=ap.action, prior_prob=ap.prob, is_chance_node=True)
                chance_node.children["heads"] = MCTSNode(
                    state_hash=f"{node.state_hash}_{ap.action}_heads",
                    parent=chance_node, action_taken=f"{ap.action}_heads", prior_prob=0.5)
                chance_node.children["tails"] = MCTSNode(
                    state_hash=f"{node.state_hash}_{ap.action}_tails",
                    parent=chance_node, action_taken=f"{ap.action}_tails", prior_prob=0.5)
                node.children[ap.action] = chance_node
            else:
                node.children[ap.action] = MCTSNode(
                    state_hash=f"{node.state_hash}_{ap.action}",
                    parent=node, action_taken=ap.action, prior_prob=ap.prob)
