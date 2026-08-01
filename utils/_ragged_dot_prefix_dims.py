
def _ragged_dot_prefix_dims(mode, rank, ragged_dim, batch, contract):
  batch, contract = map(list, (batch, contract))
  noncontract = remaining(range(rank), contract, batch)
  match mode:
    case RaggedDotMode.RAGGED_NONCONTRACTING:
      return batch + noncontract[: noncontract.index(ragged_dim)]
    case RaggedDotMode.RAGGED_CONTRACTING:
      return batch + contract[: contract.index(ragged_dim)]
    case RaggedDotMode.RAGGED_BATCH:
      return batch[: batch.index(ragged_dim)]

