
def get_proba_constraints_positivity(nus):
  A = np.zeros((nus.shape[0], 1 + nus.shape[0]))
  A[:, 1:] = -np.eye(nus.shape[0])
  return A, np.zeros(A.shape[0])


def get_proba_constraints_positivity(nus):
  A = np.zeros((nus.shape[0], 1 + nus.shape[0]))
  A[:, 1:] = -np.eye(nus.shape[0])
  return A, np.zeros(A.shape[0])

