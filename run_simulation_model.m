function simOut = run_simulation_model(dt,R,N,L)
    
    disp('simulate model using simulink');
    
    open_system('model_simulator')

    set_param('model_simulator/pos_noise','Variance',string(R));
    set_param('model_simulator/acc_noise','Variance',string(R));
    set_param('model_simulator/acc_bias','Value','0');
    set_param('model_simulator/meas_delay','DelayTime',string(dt*N));
    set_param('model_simulator/meas_disc','Frequency',string(L));
    simOut=sim('model_simulator','SimulationMode','normal','SolverType','Fixed-step','Solver','ode8','FixedStep',string(dt));

end