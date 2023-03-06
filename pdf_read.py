import matplotlib.pyplot as plt
import numpy as np

# Generate some sample EMG data
fs = 1000  # Sampling frequency (Hz)
t = np.arange(0, 1, 1/fs)  # Time vector (s)
f = 50  # EMG frequency (Hz)
emg = np.sin(2*np.pi*f*t)  # EMG signal

# Plot the EMG signal
plt.plot(t, emg)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('EMG Signal')
plt.show()
