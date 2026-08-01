
def _replica_groups_hlo(replica_groups: Sequence[Sequence[int]]
                        ) -> ir.DenseElementsAttr:
  # Uneven replica groups are padded with -1.
  groups = np.array(list(itertools.zip_longest(*replica_groups, fillvalue=-1)),
                    dtype=np.int64).T
  return ir.DenseIntElementsAttr.get(np.ascontiguousarray(groups))

