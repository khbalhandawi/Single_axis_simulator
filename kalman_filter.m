%% prep
clear all
close all
clc

%% Model (USED Tutorial: The Kalman Filter by Lacey, Tony)
dt=0.001;
R=0.000^2; %measurement noise
N = 40; % # of delayed measurements (time = N*dt)
L = 50; % # FRQUENCY of downsampled measurements for position in Hz 1000 / 50 = 40 Units 
% optimal anti-delay = ( 1 / (dt * L * 2)) + N

%% Simulate model
simOut = run_simulation_model(dt,R,N,L);
[t_out, pos_vec, vel_vec, acc_vec, pos_ds_vec] = postprocess_sim(simOut);

system('python export_sim_model.py'); % write data to text file readable by cpp application

figure
plot(pos_vec);
hold on
plot(pos_ds_vec);

xlabel('Time (s)')
ylabel('Position (m)')
legend('groundtruth','manipulated signal')

return

%% Run the filter
psi=[1 dt;0 1];
B=[(dt^2)/2 ; dt];
var_w=0.1^2;
Q=B*B'.*var_w; %prediction noise
H=[1 0];

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