import matplotlib.pyplot as plt
import control
import numpy as np
import scipy.linalg

from ovencontrol import plot_data

m = 1500   # Mass. Gives it a bit delay in the beginning.
k = 450    # Static gain. Tune so end values are similar to experimental data.
c = 240    # Time constant. Higher is slower. Damping.

# Transfer function. Static gain is numerator. Denominator is c * s + 1. dt = 1.
sys = control.tf([k], [m, c, 1])
sys = control.ss(sys)
res = scipy.linalg.expm(np.array([[sys.A[0, 0], sys.A[0, 1], sys.B[0]],
                                 [sys.A[1, 0], sys.A[1, 1], sys.B[1]],
                                 [0, 0, 0]]))
A = [[res[0, 0], res[0, 1]],
     [res[1, 0], res[1, 1]]]
B = [[res[0, 2]], [res[1, 2]]]
sys_d = control.ss(A, B, sys.C, sys.D, True)

# Plot the step responses
n = 1000  # seconds
fig, ax = plt.subplots(tight_layout=True)
for factor in [0.2, 0.3, 0.4, 0.5, 0.6, 0.8]:
    T = np.arange(0, n, 1)  # 0 -- n seconds, in steps of 1 second
    u = np.full(n, fill_value=factor)  # input vector. Step response so single value.

    y_out = np.zeros(n)
    x = np.matrix([[0], [0]])
    for i, t in enumerate(T):
        x = np.add(np.matmul(sys_d.A, x), sys_d.B * u[i])
        y_out[i] = np.add(np.matmul(sys_d.C, x), sys_d.D * u[i])

    ax.plot(T, y_out, label=str(factor))

# Plot the experimental data
ax.set_prop_cycle(None)  # Reset the color values
plot_data.plot_signals(ax)

ax.legend()

plt.show()
