# inverse_warping takes two images and a set of correspondences between
# them, and warps all the pts_initial in img_initial to the pts_final in img_final
import numpy as np
# %%
def inverse_warping(img_final, img_initial, pts_final, pts_initial):
    pts_final = np.floor(pts_final).astype(int)
    pts_initial = np.floor(pts_initial).astype(int)

    # Extract subscripts to linear indices
    ind_final = np.ravel_multi_index((pts_final[:, 1], pts_final[:, 0]), img_final.shape[0 : 2])
    ind_initial = np.ravel_multi_index((pts_initial[:, 1], pts_initial[:, 0]), img_initial.shape[0 : 2]) 


    projected_img = img_final
    
    for color in range(3):
        sub_img_final = img_final[:, :, color]
        sub_img_initial = img_initial[:, :, color]
        # Padding the goal area in video frame with logo in transparency 50%.
        sub_img_final.flat[ind_final] = sub_img_initial.flat[ind_initial] * 0.5 + sub_img_final.flat[ind_final] * 0.5
        projected_img[:, :, color] = sub_img_final

    return projected_img
