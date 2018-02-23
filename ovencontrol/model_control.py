import matplotlib.pyplot as plt
import control
import numpy as np


m = 1500   # Mass. Gives it a bit delay in the beginning.
k = 450    # Static gain. Tune so end values are similar to experimental data.
c = 240    # Time constant. Higher is slower. Damping.

# Plant transfer function. Static gain is numerator. Denominator is c * s + 1.
plant = control.tf([k], [m, c, 1])
plant_ss = control.ss(plant)

Kp = 2
Ki = 0
Kd = 1

# PID controller transfer function. C(s) = Kp + Ki/s + Kd s = (Kd s^2 + Kp s + Ki) / s
controller = control.tf([Kd, Kp, Ki], [1, 0])

sys = control.feedback(plant, controller)

# Plot the step responses
setpoint = 150
n = 100  # seconds

fig, ax = plt.subplots(tight_layout=True)
T = np.arange(0, n, 1)  # 0 -- n seconds, in steps of 1 second
u = np.full(n, fill_value=setpoint)  # input vector. Step response so single value.
T, y_out, x_out = control.forced_response(sys, T, u)
ax.plot(T, y_out, label=str(setpoint))
ax.plot(T, x_out[0], label='x0')
ax.plot(T, x_out[1], label='x1')

ax.legend()

plt.show()
