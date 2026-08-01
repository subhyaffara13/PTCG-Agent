
def _cond_key_type_signature(eqn):
  signatures = [jaxpr_type_signature(branch.jaxpr) for branch in eqn.params['branches']]
  sinks = defaultdict(list)
  sources = defaultdict(list)
  for sig in signatures:
    for sink in sig.sinks:
      sinks[sink.idx].append(sink.mask)
    for source in sig.sources:
      sources[source.idx].append(source.mask)

  combined_sinks = [Sink(i + 1, reduce(np.logical_or, m)) for i, m in sinks.items()]
  combined_sources = [Source(i, reduce(np.logical_and, m)) for i, m in sources.items()]
  combined_forwards = [Forward(f.in_idx + 1, f.out_idx) for f in
                       set.intersection(*(set(sig.forwards) for sig in signatures))]
  return KeyReuseSignature(*combined_sinks, *combined_sources, *combined_forwards)

