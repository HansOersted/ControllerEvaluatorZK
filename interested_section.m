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

%% start: 1965390, end: 1975960  and  start: 3838100, end: 3854000

interested_index_start_first = find( time_in_seconds == 1965390, 1);
interested_index_end_first = find( time_in_seconds == 1975960, 1);

interested_time_first = time_in_seconds(interested_index_start_first : interested_index_end_first);
interested_TrakingError_first = TrakingError(interested_index_start_first : interested_index_end_first);
der_interested_TrakingError_first = diff(interested_TrakingError_first)/10;
der_der_interested_TrakingError_first = diff(der_interested_TrakingError_first)/10;

interested_time_first = interested_time_first(1: end-2);
interested_TrakingError_first = interested_TrakingError_first(1: end-2);
interested_der_interested_TrakingError_first = der_interested_TrakingError_first(1: end-1);


interested_index_start_second = find( time_in_seconds == 3838100, 1);
interested_index_end_second = find( time_in_seconds == 3854000, 1);

interested_time_second = time_in_seconds(interested_index_start_second : interested_index_end_second);
interested_TrakingError_second = TrakingError(interested_index_start_second : interested_index_end_second);
der_interested_TrakingError_second = diff(interested_TrakingError_second)/10;
der_der_interested_TrakingError_second = diff(der_interested_TrakingError_second)/10;

interested_time_second = interested_time_second(1: end-2);
interested_TrakingError_second = interested_TrakingError_second(1: end-2);
interested_der_interested_TrakingError_second = der_interested_TrakingError_second(1: end-1);

interested_time = [interested_time_first; interested_time_second];
interested_TrakingError = [interested_TrakingError_first; interested_TrakingError_second];
interested_der_interested_TrakingError = [interested_der_interested_TrakingError_first; interested_der_interested_TrakingError_second];
interested_der_der_interested_TrakingError = [der_der_interested_TrakingError_first; der_der_interested_TrakingError_second];

%%

figure;
plot(interested_time, interested_TrakingError, 'b', 'DisplayName', 'Tracking Error');
xlabel('Time (seconds)');
ylabel('Value');
title('Interested Tracking Error and Its Derivative');
grid on;
hold on
plot(interested_time, interested_der_interested_TrakingError, 'r', 'DisplayName', 'Tracking Error Derivative');
hold on
plot(interested_time, interested_der_der_interested_TrakingError, 'DisplayName', 'Second Tracking Error Derivative');