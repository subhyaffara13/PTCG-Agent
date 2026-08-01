
def test_mathtext_operators():
    test_str = r'''
    \increment \smallin \notsmallowns
    \smallowns \QED \rightangle
    \smallintclockwise \smallvarointclockwise
    \smallointctrcclockwise
    \ratio \minuscolon \dotsminusdots
    \sinewave \simneqq \nlesssim
    \ngtrsim \nlessgtr \ngtrless
    \cupleftarrow \oequal \rightassert
    \rightModels \hermitmatrix \barvee
    \measuredrightangle \varlrtriangle
    \equalparallel \npreccurlyeq \nsucccurlyeq
    \nsqsubseteq \nsqsupseteq \sqsubsetneq
    \sqsupsetneq  \disin \varisins
    \isins \isindot \varisinobar
    \isinobar \isinvb \isinE
    \nisd \varnis \nis
    \varniobar \niobar \bagmember
    \triangle'''.split()

    fig = plt.figure()
    for x, i in enumerate(test_str):
        fig.text(0.5, (x + 0.5)/len(test_str), r'${%s}$' % i)

    fig.draw_without_rendering()

