
def gamma_correct(rgba_0_255, gamma):
    corrected = round(255.0 * math.pow(rgba_0_255 / 255.0, gamma))
    return max(min(int(corrected), 255), 0)

