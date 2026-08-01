
def _gamma_trace1(*a):
    gctr = 4  # FIXME specific for d=4
    g = LorentzIndex.metric
    if not a:
        return gctr
    n = len(a)
    if n%2 == 1:
        #return TensMul.from_data(S.Zero, [], [], [])
        return S.Zero
    if n == 2:
        ind0 = a[0].get_indices()[0]
        ind1 = a[1].get_indices()[0]
        return gctr*g(ind0, ind1)
    if n == 4:
        ind0 = a[0].get_indices()[0]
        ind1 = a[1].get_indices()[0]
        ind2 = a[2].get_indices()[0]
        ind3 = a[3].get_indices()[0]

        return gctr*(g(ind0, ind1)*g(ind2, ind3) - \
           g(ind0, ind2)*g(ind1, ind3) + g(ind0, ind3)*g(ind1, ind2))

