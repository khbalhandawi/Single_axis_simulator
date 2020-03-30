%% prep
clear all
close all
clc

%% Model (USED Tutorial: The Kalman Filter by Lacey, Tony)
dt=0.001;
psi=[1 dt;0 1];
B=[(dt^2)/2 ; dt];
var_w=0.1^2;
Q=B*B'.*var_w; %prediction noise
H=[1 0];
R=0.001^2; %measurement noise
N = 20; % # of delayed measurements (time = N*dt)
L = 50; % # of downsampled measurements

%% Simulate model
simOut = run_simulation_model(dt,R,N,L);
[t_out, pos_vec, vel_vec, acc_vec, pos_ds_vec] = postprocess_sim(simOut);

system('python export_sim_model.py'); % write data to text file readable by cpp application

figure
plot(pos_vec);
hold on
plot(pos_ds_vec);

return

%% Run the filter
x_0=[0 0]; % Initial estimator states
x = SPKF(acc_vec,pos_ds_vec,x_0,B,H,N,R,psi);

%% plot stuff
plot(x(1,:));
hold on
plot(pos_vec);
figure
plot(x(2,:));
hold on
plot(vel_vec);