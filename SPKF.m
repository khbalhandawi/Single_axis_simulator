function [x] = SPKF(acc_data,pos_data,x_0,B,H,N,R,psi)
    x=zeros(length(x_0),length(acc_data));
    x(:,1)=x_0;
    P=[1 0;0 1];
    for i=2:length(acc_data)
        %predict:
        x(:,i)=psi*x(:,i-1)+B*acc_data(i-1);
        P=psi*P*psi';
        %measure:
        S=H * P*H'+R;
        K=(P*H')/S;
        x(:,i)=x(:,i)+K*(pos_data(i)-H*x(:,i));
        P=(eye(length(P))-K*H)*P;
    end
    %% Filter with delayed measurement (TODO: by Khalil and Saif)
    % Please take care of:
    % 1. for sample-and-hold make sure you are taking the measurement at the
    % very beginning of the hold.

    x=zeros(length(x_0),length(acc_data));
    x(:,1)=x_0;

    P=[1 0;0 1];
    P_mem=zeros(size(P,1),size(P,2),N);
    for i=2:length(acc_data)
        %predict:
        x(:,i)=psi*x(:,i-1)+B*acc_data(i-1);
        P=psi*P*psi';
        %measure:
        S=H * P*H'+R;
        K=(P*H')/S;
        x(:,i)=x(:,i)+K*(pos_data(i)-H*x(:,i));
        P=(eye(length(P))-K*H)*P;
        %re-predict
    end
end