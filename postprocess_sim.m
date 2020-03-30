function [t_out, pos_vec_1D, vel_vec_1D, acc_vec_1D, pos_ds_vec_1D] = postprocess_sim(simOut)
   t_out = simOut.tout;
    
    pos_vec_1D = simOut.x_true.data;
    vel_vec_1D = simOut.x_dot_true.data;
    acc_vec_1D = simOut.u_acc.data;
    pos_ds_vec_1D = simOut.y_obs.data;

    chanel = 2;
    
    pos_vec = zeros(length(simOut.x_true.data),3);
    pos_vec(:,chanel) = simOut.x_true.data;

    vel_vec = zeros(length(simOut.x_dot_true.data),3);
    vel_vec(:,chanel) = simOut.x_dot_true.data;

    acc_vec = zeros(length(simOut.u_acc.data),3);
    acc_vec(:,chanel) = simOut.u_acc.data;

    pos_ds_vec = zeros(length(simOut.y_obs.data),3);
    pos_ds_vec(:,chanel) = simOut.y_obs.data;

    optitack_imu_data = [t_out, pos_vec, vel_vec, acc_vec, pos_ds_vec]';

    save('optitrack_Data.mat','optitack_imu_data')
end

