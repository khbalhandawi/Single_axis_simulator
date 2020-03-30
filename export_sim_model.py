
# -*- coding: utf-8 -*-
"""
Spyder Editor

"""

# -------------------------------------------------------
from numpy import pi
import numpy as np
import scipy.io
import matplotlib.pyplot as plt

def load_raw_data(filename):
    
    mat = scipy.io.loadmat(filename) # get optitrack data
    data = mat['optitack_imu_data']
    [t_raw_a, x_a, y_a, z_a, vx_a, vy_a, vz_a, ax_a, ay_a, az_a, x_ds, y_ds, z_ds] = data
    
    ax_out = []; ay_out = []; az_out = []
    mx_out = []; my_out = []; mz_out = []
    gx_a = []; gy_a = []; gz_a = []
    roll_a = []; pitch_a = []; yaw_a = []
    roll_ds = []; pitch_ds = []; yaw_ds = []
    g = 9.81
    
    for t_raw, x, y, z, vx, vy, vz, ax, ay, az in zip(t_raw_a, x_a, y_a, z_a, vx_a, vy_a, vz_a, ax_a, ay_a, az_a):
    
        ax_out += [ax/g]; ay_out += [ay/g]; az_out += [az/g]
        mx_out += [0.0]; my_out += [0.0]; mz_out += [0.0]
        gx_a += [0.0]; gy_a += [0.0]; gz_a += [0.0]
        roll_a += [0.0]; pitch_a += [0.0]; yaw_a += [0.0]
        roll_ds += [0.0]; pitch_ds += [0.0]; yaw_ds += [0.0]
    ## FLUSH TO STERR
    #stderr.write("""\r t = %s s |  (ax,ay,az) = (%f,%f,%f) m/s^2
    #                \r t = %s s |  (gx,gy,gz) = (%f,%f,%f) rad/s
    #                \r t = %s s |  (mx,my,mz) = (%f,%f,%f) m/s^2
    #                \r t = %s s |  (roll,pitch,yaw) = (%f,%f,%f) deg"""
    #             % (t, ax, ay, az, t, gx, gy, gz, t, mx, my, mz, t, roll * (180.0 / pi), pitch * (180.0 / pi), yaw * (180.0 / pi)) )
    #stderr.flush()
    
    data_out = [t_raw_a, x_a, y_a, z_a, roll_a, pitch_a, yaw_a, 
                roll_ds, pitch_ds, yaw_ds, x_ds, y_ds, z_ds, 
                vx_a, vy_a, vz_a, 
                ax_out, ay_out, az_out, gx_a, gy_a, gz_a, mx_out, my_out, mz_out]
    
    return data_out

def export_modified_data(filename,IMU_data,Raw_position_data,Raw_velocity_data,ds_data,display_out):

    [t_a, ax_a, ay_a, az_a, gx_a, gy_a, gz_a, mx_a, my_a, mz_a] = IMU_data
    [t_a, x_a, y_a, z_a, roll_a, pitch_a, yaw_a] = Raw_position_data
    [vx_a, vy_a, vz_a] = Raw_velocity_data
    [roll_ds,pitch_ds,yaw_ds,x_ds,y_ds,z_ds] = ds_data
    
    data_write_out = [ax_a, ay_a, az_a, gx_a, gy_a, gz_a, mx_a, my_a, mz_a, roll_ds, pitch_ds, yaw_ds, x_ds, y_ds, z_ds, roll_a, pitch_a, yaw_a, x_a, y_a, z_a, vx_a, vy_a, vz_a, t_a]
    data_write_out = list(map(list, zip(*data_write_out))) # transpose a list of lists
    
    with open(filename, "w", newline=None) as f:
        np.savetxt(filename, data_write_out, delimiter=" ", fmt = "%.8e", newline='\n')
    
    # read data from file
    resultsfile=open(filename,'r')
    lines = resultsfile.readlines()
    
    # REMOVE LAST EMPTY LINE VERY IMP for C++
    resultsfile.close()
    w = open(filename,'w')
    
    lines[-1] = lines[-1][0:-1]
    w.writelines([item for item in lines])
    
    w.close()
    # !!!!
    
    if display_out:
    
        # Plot down sampled Raw data
        my_dpi = 100
        plt.figure(figsize=(1200/my_dpi, 500/my_dpi), dpi=my_dpi)
        plt.title("x y z comparision")
        plt.subplot(1, 3, 1)
        plt.plot(t_a, x_ds, "k", label = "Downsampled")
        plt.plot(t_a, x_a, "r", label = "Groundtruth")
        
        plt.title("x")
        plt.legend()
        
        plt.subplot(1, 3, 2)
        plt.plot(t_a, y_ds, "k", label = "Downsampled")
        plt.plot(t_a, y_a, "r", label = "Groundtruth")
        
        plt.title("y")
        plt.legend()
        
        plt.subplot(1, 3, 3)
        plt.plot(t_a, z_ds, "k", label = "Downsampled")
        plt.plot(t_a, z_a, "r", label = "Groundtruth")
        
        plt.title("z")
        plt.legend()
        plt.show()

def run_single_axis_simulation():
    import matlab.engine
    import numpy as np

    dt = 0.001
    psi = np.array([ [1, dt], [0, 1] ])
    B = np.array([(dt**2)/2, dt])
    var_w = 0.1**2

    Q = (B * B.T) * var_w #prediction noise
    H = np.array([1, 0])
    R = 0.001**2 # measurement noise
    N = 40 # of delayed measurements (time = N*dt)
    L = 5 # of downsampled measurements

    eng = matlab.engine.start_matlab()
    ret = eng.run_simulation_model(dt,R,N,L)

def main():

    plt.close('all') # close all existing figures
    
    # run_single_axis_simulation()

    filename = 'optitrack_Data.mat'
    [t_raw_a, 
     x_a, y_a, z_a, roll_a, pitch_a, yaw_a, 
     roll_ds, pitch_ds, yaw_ds, x_ds, y_ds, z_ds, 
     vx_a, vy_a, vz_a, 
     ax_a, ay_a, az_a, gx_a, gy_a, gz_a, mx_a, my_a, mz_a] = load_raw_data(filename)
    
    IMU_data = [t_raw_a, ax_a, ay_a, az_a, gx_a, gy_a, gz_a, mx_a, my_a, mz_a]
    Raw_position_data = [t_raw_a, x_a, y_a, z_a, roll_a, pitch_a, yaw_a]
    Raw_velocity_data = [vx_a, vy_a, vz_a]
    
    ds_data = [roll_ds,pitch_ds,yaw_ds,x_ds,y_ds,z_ds]
    
    # export modified data to file
    filename = "NAV3_data.bin"
    export_modified_data(filename,IMU_data,Raw_position_data,Raw_velocity_data,ds_data,False)
    
if __name__ == "__main__":
    main()

#-------------------------------------------------------