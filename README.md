# Single_axis_simulator

This project is aimed at estimating drone position and velocity using sensor fusion of IMU measurements with position trackers.

# Installation

- Launch "kalman_filter.m":
- Set the following parameters:
  - dt=0.001;
  - R=0.001^2; %measurement noise
  - N = 20; % # of delayed measurements (time = N*dt)
  - L = 50; % # of downsampled measurements

- Use NAV3_data.bin file as input data for SMO_filter application
