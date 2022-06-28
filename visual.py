def project_points(cld,pred_rt,debug=False):
    cam_cx = 321.8757019042969
    cam_cy = 240.312744140625
    cam_fx = 386.03887939453125
    cam_fy = 386.03887939453125
    if debug:
        cam_cx = 312.9869
        cam_cy = 241.3109
        cam_fx = 1066.778
        cam_fy = 1067.487
    pred_t=np.array([pred_rt[0][3], pred_rt[1][3], pred_rt[2][3]])
    # pred_model = transform(pred_rt[:4],pred_rt[4:],cld)
    pred_model=np.add(np.dot(cld,pred_rt[:3, :3].T),pred_t)
    pred_model_x=pred_model[:,0]
    pred_model_y=pred_model[:,1]
    pred_model_z=pred_model[:,2]
    # x = ((pred_model_x * cam_fx) / pred_model_z) + cam_cx
    # y = ((pred_model_y * cam_fy) / pred_model_z) + cam_cy
    # project_xy=np.concatenate((x[:,None],y[:,None]),axis=1)
    project_x = (((pred_model_x * cam_fx) / pred_model_z) + cam_cx).astype(np.int32)
    project_y = (((pred_model_y * cam_fy) / pred_model_z) + cam_cy).astype(np.int32)
    project_y_1 = project_y[np.logical_and(project_y < 480, project_y > 0)]
    project_x_1 = project_x[np.logical_and(project_y < 480, project_y > 0)]
    project_z_1 = pred_model_z[np.logical_and(project_y < 480, project_y > 0)]
    project_x_2 = project_x_1[np.logical_and(project_x_1 < 640, project_x_1 > 0)]
    project_y_2 = project_y_1[np.logical_and(project_x_1 < 640, project_x_1 > 0)]
    project_z_2 = project_z_1[np.logical_and(project_x_1 < 640, project_x_1 > 0)]
    return project_x_2,project_y_2
    
def visual_pic(project_x,project_y,cv_img):
    # pic=Image.fromarray(np.array(cv_img))
    # plt.scatter(project_x,project_y, alpha=0.6)
    # plt.imshow(pic, alpha=0.4)
    # plt.show()
    np_img=np.array(cv_img,dtype=np.uint8)
    project_y_1 = project_y[np.logical_and(project_y < 480, project_y > 0)]
    project_x_1 = project_x[np.logical_and(project_y < 480, project_y > 0)]
    project_x_2 = project_x_1[np.logical_and(project_x_1 < 640, project_x_1 > 0)]
    project_y_2 = project_y_1[np.logical_and(project_x_1 < 640, project_x_1 > 0)]
    np_img[np.array(project_y_2,dtype=np.int32),np.array(project_x_2,dtype=np.int32),0]=0
    np_img[np.array(project_y_2, dtype=np.int32),np.array(project_x_2, dtype=np.int32),  1] = 0
    np_img[np.array(project_y_2, dtype=np.int32),np.array(project_x_2, dtype=np.int32),  2] = 255
    cv2.imshow('color',np_img)
    cv2.waitKey(0)