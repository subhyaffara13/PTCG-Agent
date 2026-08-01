
def mi_rank(score):
    r'''Rank the score with a letter:

        * A if :math:`\text{score} > 19`;
        * B if :math:`9 < \text{score} \le 19`;
        * C if :math:`\text{score} \le 9`.
    '''
    return chr(65 + (9 - score >= 0) + (19 - score >= 0))

