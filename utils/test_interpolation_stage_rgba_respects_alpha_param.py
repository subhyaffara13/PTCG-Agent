
def test_interpolation_stage_rgba_respects_alpha_param(fig_test, fig_ref, intp_stage):
    axs_tst = fig_test.subplots(2, 3)
    axs_ref = fig_ref.subplots(2, 3)
    ny, nx = 3, 3
    scalar_alpha = 0.5
    array_alpha = np.random.rand(ny, nx)

    # When the image does not have an alpha channel, alpha should be specified
    # by the user or default to 1.0
    im_rgb = np.random.rand(ny, nx, 3)
    im_concat_default_a = np.ones((ny, nx, 1))  # alpha defaults to 1.0
    im_rgba = np.concatenate(  # combine rgb channels with array alpha
        (im_rgb, array_alpha.reshape((ny, nx, 1))), axis=-1
    )
    axs_tst[0][0].imshow(im_rgb)
    axs_ref[0][0].imshow(np.concatenate((im_rgb, im_concat_default_a), axis=-1))
    axs_tst[0][1].imshow(im_rgb, interpolation_stage=intp_stage, alpha=scalar_alpha)
    axs_ref[0][1].imshow(
        np.concatenate(  # combine rgb channels with broadcasted scalar alpha
            (im_rgb, scalar_alpha * im_concat_default_a), axis=-1
        ), interpolation_stage=intp_stage
    )
    axs_tst[0][2].imshow(im_rgb, interpolation_stage=intp_stage, alpha=array_alpha)
    axs_ref[0][2].imshow(im_rgba, interpolation_stage=intp_stage)

    # When the image already has an alpha channel, multiply it by the
    # alpha param (both scalar and array alpha multiply the existing alpha)
    axs_tst[1][0].imshow(im_rgba)
    axs_ref[1][0].imshow(im_rgb, alpha=array_alpha)
    axs_tst[1][1].imshow(im_rgba, interpolation_stage=intp_stage, alpha=scalar_alpha)
    axs_ref[1][1].imshow(
        np.concatenate(  # combine rgb channels with scaled array alpha
            (im_rgb, scalar_alpha * array_alpha.reshape((ny, nx, 1))), axis=-1
        ), interpolation_stage=intp_stage
    )
    new_array_alpha = np.random.rand(ny, nx)
    axs_tst[1][2].imshow(im_rgba, interpolation_stage=intp_stage, alpha=new_array_alpha)
    axs_ref[1][2].imshow(
        np.concatenate(  # combine rgb channels with multiplied array alpha
            (im_rgb, array_alpha.reshape((ny, nx, 1))
             * new_array_alpha.reshape((ny, nx, 1))), axis=-1
        ), interpolation_stage=intp_stage
    )

