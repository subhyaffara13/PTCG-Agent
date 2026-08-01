
def get_all_nn_module_tests():
    # additional modules test
    # TODO: delete this list once we make all nn_tests work
    additional_module_tests = [
        {
            'module_name': 'Bilinear',
            'constructor_args': (S, S, M),
            'input_size': (S, S),
            'extra_args': ((S, S),)
        },
        {
            'module_name': 'RNNCell',
            'constructor_args': (S, S),
            'input_size': (S, S),
        },
        {
            'module_name': 'LSTMCell',
            'constructor_args': (S, S),
            'input_size': (S, S),
        },
        {
            'module_name': 'GRUCell',
            'constructor_args': (S, S),
            'input_size': (S, S),
        },
        {
            'module_name': 'MultiheadAttention',
            'constructor_args': (128, 8),
            'input_size': (10, 8, 128),
            'extra_args': (torch.randn(10, 8, 128), torch.randn(10, 8, 128)),
            'slowTest': True
        },
        {
            'module_name': 'Transformer',
            'constructor_args': (1, 1, 1, 1, 2),
            'input_size': (3, 1, 1),
            'extra_args': (torch.randn(1, 1, 1),),
            'slowTest': True
        }
    ]

    return module_tests + get_new_module_tests() + additional_module_tests

