
def _num_himuts_out(final_qdds):
  return sum(len(a.lo_ty()) for a in final_qdds if a.has_qdd)

