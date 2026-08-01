
def _get_neural_network():
    global _nn_instance
    if _nn_instance is None:
        try:
            from cb_agents.value_network import NeuralValueNetwork
            _nn_instance = NeuralValueNetwork()
        except Exception as e:
            logger.warning(f"Failed to instantiate NeuralValueNetwork: {e}")
    return _nn_instance


def _get_neural_network():
    global _nn_instance
    if _nn_instance is None:
        try:
            from cb_agents.value_network import NeuralValueNetwork
            _nn_instance = NeuralValueNetwork()
        except Exception as e:
            logger.warning(f"Failed to instantiate NeuralValueNetwork: {e}")
    return _nn_instance

