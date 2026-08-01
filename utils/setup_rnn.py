
def setup_rnn(use_input_variant, args, kwargs):
    with (
        batch_second(args, kwargs)
        if use_input_variant
        else allow_smaller_batches(args, kwargs)
    ):
        yield

