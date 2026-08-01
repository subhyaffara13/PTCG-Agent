
def _create_basic_net():
    class Layer(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.layer_dummy_param = nn.Parameter(torch.empty(3, 5))
            self.layer_dummy_buf = nn.Buffer(torch.zeros(1, 3, 3, 7))

    class Net(nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.l1 = Layer()
            self.dummy_param = nn.Parameter(torch.empty(3, 5))
            self.dummy_buf = nn.Buffer(torch.zeros(7, 3, 3, 1))

    l = Layer()
    n = Net()
    s = nn.Sequential(n, n)

    return l, n, s

