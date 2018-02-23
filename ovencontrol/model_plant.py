import matplotlib.pyplot as plt
import control
import numpy as np

from ovencontrol import plot_data

m = 1500   # Mass. Gives it a bit delay in the beginning.
k = 450    # Static gain. Tune so end values are similar to experimental data.
c = 240    # Time constant. Higher is slower. Damping.

# Transfer function. Static gain is numerator. Denominator is c * s + 1.
sys = control.tf([k], [m, c, 1])

# Plot the step responses
n = 1000  # seconds
fig, ax = plt.subplots(tight_layout=True)
for factor in [0.2, 0.3, 0.4, 0.5, 0.6, 0.8]:
    T = np.arange(0, n, 1)  # 0 -- n seconds, in steps of 1 second
    u = np.full(n, fill_value=factor)  # input vector. Step response so single value.
    T, y_out, x_out = control.forced_response(sys, T, u)
    ax.plot(T, y_out, label=str(factor))

# Plot the experimental data
ax.set_prop_cycle(None)  # Reset the color values
plot_data.plot_signals(ax)

ax.legend()

plt.show()
