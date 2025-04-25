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

TrakingError = TIC3011_SV - TIC3011_PV;

%% start: 1965390, end: 1975960
interested_index_start = find( time_in_seconds == 1965390, 1);
interested_index_end = find( time_in_seconds == 1975960, 1);

interested_time = time_in_seconds(interested_index_start : interested_index_end);
interested_TrakingError = TrakingError(interested_index_start : interested_index_end);
der_interested_TrakingError = diff(interested_TrakingError)/10;

interested_time = interested_time(1: end-1);
interested_TrakingError = interested_TrakingError(1: end-1);

%%

figure;
plot(interested_time, interested_TrakingError, 'b', 'DisplayName', 'Tracking Error');
xlabel('Time (seconds)');
ylabel('Value');
title('Interested Tracking Error and Its Derivative');
grid on;
hold on
plot(interested_time, der_interested_TrakingError, 'r', 'DisplayName', 'Tracking Error Derivative');