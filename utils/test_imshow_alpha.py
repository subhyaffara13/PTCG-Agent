
def test_imshow_alpha(fig_test, fig_ref):
    np.random.seed(19680801)

    rgbf = np.random.rand(6, 6, 3).astype(np.float32)
    rgbu = np.uint8(rgbf * 255)
    ((ax0, ax1), (ax2, ax3)) = fig_test.subplots(2, 2)
    ax0.imshow(rgbf, alpha=0.5)
    ax1.imshow(rgbf, alpha=0.75)
    ax2.imshow(rgbu, alpha=127/255)
    ax3.imshow(rgbu, alpha=191/255)

    rgbaf = np.concatenate((rgbf, np.ones((6, 6, 1))), axis=2).astype(np.float32)
    rgbau = np.concatenate((rgbu, np.full((6, 6, 1), 255, np.uint8)), axis=2)
    ((ax0, ax1), (ax2, ax3)) = fig_ref.subplots(2, 2)
    rgbaf[:, :, 3] = 0.5
    ax0.imshow(rgbaf)
    rgbaf[:, :, 3] = 0.75
    ax1.imshow(rgbaf)
    rgbau[:, :, 3] = 127
    ax2.imshow(rgbau)
    rgbau[:, :, 3] = 191
    ax3.imshow(rgbau)

