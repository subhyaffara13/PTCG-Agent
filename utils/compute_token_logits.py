
def compute_token_logits(sequence_output, temperature, output_weights, output_bias):
    """
    Computes logits per token

    Args:
        sequence_output (`torch.FloatTensor` of shape `(batch_size, sequence_length, hidden_size)`):
            Also known as last_hidden_state. Sequence of hidden-states at the output of the last layer of the model.
        temperature (`float`):
            Temperature for the Bernoulli distribution.
        output_weights (`torch.FloatTensor` of shape `(hidden_size,)`):
            Weights of the linear layer for cell selection.
        output_bias (`torch.FloatTensor` of shape `()`):
            Bias of the linear layer for cell selection

    Returns:
        logits (`torch.FloatTensor` of shape `(batch_size, sequence_length)`): Logits per token.
    """
    logits = (torch.einsum("bsj,j->bs", sequence_output, output_weights) + output_bias) / temperature

    return logits

