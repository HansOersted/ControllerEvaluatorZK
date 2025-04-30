import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

filename = '1号大塔20241201至20250301历史趋势.csv'
df = pd.read_csv(filename, encoding='gbk')

# 第二列是时间字符串
time_str = df.iloc[:, 1].astype(str).str.strip()
time = pd.to_datetime(time_str, format='%Y-%m-%d %H:%M:%S')

# w.r.t. the first time point
time_in_seconds = (time - time.iloc[0]).dt.total_seconds()

#  read TIC3011_PV and TIC3011_SV
TIC3011_PV = df.iloc[:, 9]
TIC3011_SV = df.iloc[:, 10]

TrackingError = TIC3011_SV - TIC3011_PV

interested_index_start = time_in_seconds[time_in_seconds == 1965390].index[0]
interested_index_end = time_in_seconds[time_in_seconds == 1975960].index[0]

interested_time = time_in_seconds[interested_index_start : interested_index_end + 1].reset_index(drop=True)
interested_TrackingError = TrackingError[interested_index_start : interested_index_end + 1].reset_index(drop=True)

# first and second order derivatives
der_interested_TrackingError = interested_TrackingError.diff().iloc[1:].reset_index(drop=True) / 10
der_der_interested_TrackingError = der_interested_TrackingError.diff().iloc[1:].reset_index(drop=True) / 10

# align the lengths
interested_time = interested_time.iloc[:-2].reset_index(drop=True)
interested_TrackingError = interested_TrackingError.iloc[:-2].reset_index(drop=True)
interested_der_interested_TrackingError = der_interested_TrackingError.iloc[:-1].reset_index(drop=True)

plt.figure()
plt.plot(interested_time, interested_TrackingError, 'b', label='Tracking Error')
plt.plot(interested_time, interested_der_interested_TrackingError, 'r', label='Tracking Error Derivative')
plt.plot(interested_time, der_der_interested_TrackingError, label='Second Tracking Error Derivative')
plt.xlabel('Time (seconds)')
plt.ylabel('Value')
plt.title('Interested Tracking Error and Its Derivative')
plt.grid(True)
plt.legend()
plt.show()
