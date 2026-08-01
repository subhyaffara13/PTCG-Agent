
def test_MIMOFeedback_printing():
    tf1 = TransferFunction(1, s, s)
    tf2 = TransferFunction(s, s**2 - 1, s)
    tf3 = TransferFunction(s, s - 1, s)
    tf4 = TransferFunction(s**2, s**2 - 1, s)

    tfm_1 = TransferFunctionMatrix([[tf1, tf2], [tf3, tf4]])
    tfm_2 = TransferFunctionMatrix([[tf4, tf3], [tf2, tf1]])

    # Negative Feedback (Default)
    assert latex(MIMOFeedback(tfm_1, tfm_2)) == \
        r'\left(I_{\tau} + \left[\begin{matrix}\frac{1}{s} & \frac{s}{s^{2} - 1}\\\frac{s}{s - 1} & \frac{s^{2}}{s^{2} - 1}\end{matrix}\right]_\tau\cdot\left[' \
        r'\begin{matrix}\frac{s^{2}}{s^{2} - 1} & \frac{s}{s - 1}\\\frac{s}{s^{2} - 1} & \frac{1}{s}\end{matrix}\right]_\tau\right)^{-1} \cdot \left[\begin{matrix}' \
        r'\frac{1}{s} & \frac{s}{s^{2} - 1}\\\frac{s}{s - 1} & \frac{s^{2}}{s^{2} - 1}\end{matrix}\right]_\tau'

    # Positive Feedback
    assert latex(MIMOFeedback(tfm_1*tfm_2, tfm_1, 1)) == \
        r'\left(I_{\tau} - \left[\begin{matrix}\frac{1}{s} & \frac{s}{s^{2} - 1}\\\frac{s}{s - 1} & \frac{s^{2}}{s^{2} - 1}\end{matrix}\right]_\tau\cdot\left' \
        r'[\begin{matrix}\frac{s^{2}}{s^{2} - 1} & \frac{s}{s - 1}\\\frac{s}{s^{2} - 1} & \frac{1}{s}\end{matrix}\right]_\tau\cdot\left[\begin{matrix}\frac{1}{s} & \frac{s}{s^{2} - 1}' \
        r'\\\frac{s}{s - 1} & \frac{s^{2}}{s^{2} - 1}\end{matrix}\right]_\tau\right)^{-1} \cdot \left[\begin{matrix}\frac{1}{s} & \frac{s}{s^{2} - 1}' \
        r'\\\frac{s}{s - 1} & \frac{s^{2}}{s^{2} - 1}\end{matrix}\right]_\tau\cdot\left[\begin{matrix}\frac{s^{2}}{s^{2} - 1} & \frac{s}{s - 1}\\\frac{s}{s^{2} - 1}' \
        r' & \frac{1}{s}\end{matrix}\right]_\tau'

