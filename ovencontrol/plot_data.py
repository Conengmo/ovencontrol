import os
import numpy as np
import matplotlib.pyplot as plt

from ovencontrol import open_data


TEMPERATURE_ORIGIN = 0


def reset_origin(temperature):
    current_origin = np.min(temperature[:5])
    temperature[:] = temperature - (current_origin - TEMPERATURE_ORIGIN)


def main():
    tests, test_random = open_data.retrieve_data(os.path.join('..', 'data'))
    fig, ax = plt.subplots()
    for key in sorted(tests.keys()):
        res = tests[key]
        reset_origin(res.temperature)
        ax.plot(res.time, res.temperature, label=key)
    ax.legend()
    ax.set_ylabel('Temperature increase (deg C)')
    ax.set_xlabel('Seconds since start')
    # save(fig, filename='tests')


def plot_linearity():
    tests, test_random = open_data.retrieve_data(os.path.join('..', 'data'))
    fig, ax = plt.subplots()
    for key in sorted(tests.keys()):
        res = tests[key]
        reset_origin(res.temperature)
        max_output = np.max(res.temperature)
        ax.plot(res.duty_cycle, max_output / res.duty_cycle, 'x')
    ax.set_xlabel('Duty cycle')
    ax.set_ylabel('Temperature / duty cycle')
    ax.set_title('Steady-state gain over input')
    # save(fig, filename='linearity.png')


def save(fig, filename=None, path=None):
    """Save the figure to disk as PNG."""
    fig.tight_layout()
    if filename is None:
        filename = '_fig.png'
    if path is None:
        path = os.path.join('..', 'graphs')
    if not os.path.exists(path):
        os.makedirs(path)
    fig.savefig(os.path.join(path, filename), dpi=300)


if __name__ == '__main__':
    main()
    # plot_linearity()
    plt.show()
