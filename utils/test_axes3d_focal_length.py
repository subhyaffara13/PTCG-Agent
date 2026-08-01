
def test_axes3d_focal_length():
    fig, axs = plt.subplots(1, 2, subplot_kw={'projection': '3d'})
    axs[0].set_proj_type('persp', focal_length=np.inf)
    axs[1].set_proj_type('persp', focal_length=0.15)

