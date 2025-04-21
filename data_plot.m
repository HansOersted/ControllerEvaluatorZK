clear
close all

%%
filename = '1号大塔20241201至20250301历史趋势.csv';

T = readtable(filename, 'PreserveVariableNames', true);

time_str = T{:, 2};  % time string (the second column)
time = datetime(time_str, 'InputFormat', 'yyyy-MM-dd HH:mm:ss');

% w.r.t. the first time point
time_in_seconds = seconds(time - time(1));

TIC3011_PV = T{:, 10};  % actual value
TIC3011_SV = T{:, 11};  % reference

figure;
plot(time_in_seconds, TIC3011_PV, 'b', 'DisplayName', 'TIC3011.PV (Actual)');
hold on;
plot(time_in_seconds, TIC3011_SV, 'r--', 'DisplayName', 'TIC3011.SV (Reference)');
xlabel('Time (seconds)');
ylabel('Value');
legend;
title('TIC3011 Actual vs Reference Trend');
grid on;