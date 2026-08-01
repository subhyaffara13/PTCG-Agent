
def sample_inputs_ctc_loss(op_info, device, dtype, requires_grad, **kwargs):
    input_length = 50
    batch = 16
    num_char = 20
    target_length = 30

    def make_log_probs(s):
        t = make_tensor(s, device=device, dtype=dtype)
        log_probs = t.log_softmax(2).to(device=device, dtype=dtype).detach().requires_grad_(requires_grad=requires_grad)
        return log_probs

    reductions = ('none', 'mean', 'sum')
    zero_inf = (True, False)
    lengths_type = (list, torch.Tensor)
    for r, z, lt in product(reductions, zero_inf, lengths_type):
        log_probs = make_log_probs((input_length, batch, num_char))
        targets = torch.randint(1, num_char, (batch, target_length), dtype=torch.long, device=device)
        input_lengths = torch.full((batch, ), input_length, dtype=torch.long, device=device)
        target_lengths = torch.randint(10, target_length, (batch, ), dtype=torch.long, device=device)

        # Dont generate int[] types if reduction = "Mean" since this results in non composite compliant calls
        # to ctc_loss.IntList since a tensor needs to be created from the target lengths.
        # Creating such a tensor requires the use of pointers to copy data from int[] -> torch.Tensor
        # e.g. via std::copy. Similarly symbolic/real tracing with fx will also not work
        if lt is list and r in ["none", "sum"]:
            input_lengths = input_lengths.tolist()
            target_lengths = target_lengths.tolist()

        yield SampleInput(log_probs, args=(targets, input_lengths, target_lengths,),
                          kwargs=dict(reduction=r, zero_infinity=z))

