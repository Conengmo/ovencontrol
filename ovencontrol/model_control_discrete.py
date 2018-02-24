import matplotlib.pyplot as plt
import control
import numpy as np
import scipy.linalg


class PID:
    """Discrete PID control"""
    def __init__(self, Kp, Ki, Kd, u_max=None, u_min=None, integrator_max=None, integrator_min=None):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.u_max = u_max
        self.u_min = u_min
        self.error_previous = 0
        self.integrator = 0
        self.integrator_max = integrator_max
        self.integrator_min = integrator_min
        self.setpoint = 0.0

    def get_control_input(self, current_value):
        """Calculate PID output value for given reference input and feedback"""
        error = self.setpoint - current_value

        p_value = self.Kp * error

        d_value = self.Kd * (error - self.error_previous)
        self.error_previous = error

        self.integrator += error
        if self.integrator_max is not None:
            self.integrator = min([self.integrator, self.integrator_max])
        if self.integrator_min is not None:
            self.integrator = max([self.integrator, self.integrator_min])
        i_value = self.Ki * self.integrator

        u = p_value + i_value + d_value
        if self.u_max is not None:
            u = min([u, self.u_max])
        if self.u_min is not None:
            u = max([u, self.u_min])
        return u


def main():
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

    Kp = 0.1
    Ki = 0
    Kd = 2

    pid = PID(Kp, Ki, Kd, u_max=1, u_min=0)

    timestep_control = 2
    ts = 1
    r = np.concatenate((np.arange(50, 150, 50 / (120 // ts)),
                        np.arange(150, 180, 30 / (80 // ts)),
                        np.arange(180, 240, 60 / (60 // ts)),
                        np.arange(240, 0, -240 / (60 // ts)),
                        ))
    n = len(r)

    T = np.arange(0, n, ts)
    # r = np.full(n, fill_value=150)  # input vector. Step response so single value.
    y = np.zeros(n)
    u = np.zeros(n)
    x = np.matrix([[0], [0]])
    y_prev = 0
    time_since_control_update = 9000

    for i, t in enumerate(T):
        time_since_control_update += t
        if time_since_control_update >= timestep_control:
            pid.setpoint = r[i]
            u[i] = pid.get_control_input(y_prev)
            time_since_control_update = 0
        else:
            u[i] = u[i - 1]
        x = np.add(np.matmul(sys_d.A, x), sys_d.B * u[i])
        y[i] = np.add(np.matmul(sys_d.C, x), sys_d.D * u[i])
        y_prev = y[i]

    fig, axs = plt.subplots(2, 1, sharex=True, tight_layout=True)
    axs[0].plot(T, y, label='y')
    axs[0].plot(T, r, label='r')
    axs[0].legend()
    axs[1].plot(T, u)


if __name__ == '__main__':
    main()
    plt.show()
