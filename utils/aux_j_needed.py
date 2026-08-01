
def aux_J_needed(ctx, xA, xeps4, a, xB1, xM):
    #  DETERMINATION OF  J  THE NUMBER OF TERMS NEEDED
    #            IN THE TAYLOR SERIES OF F.
    #  See II Section 3.11 equation (49))
    #  Only determine one
    h1 = xeps4/(632*xA)
    h2 = xB1*a * 126.31337419529260248  # = pi^2*e^2*sqrt(3)
    h2 = h1 * ctx.power((h2/xM**2),(xM-1)/3) / xM
    h3 = min(h1,h2)
    return h3

