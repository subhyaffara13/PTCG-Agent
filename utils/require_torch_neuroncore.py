
def require_torch_neuroncore(test_case):
    """
    Decorator marking a test that requires NeuronCore (in PyTorch).
    """
    return unittest.skipUnless(is_torch_neuroncore_available(check_device=False), "test requires PyTorch NeuronCore")(
        test_case
    )

