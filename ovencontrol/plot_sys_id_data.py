import os
import numpy as np
import matplotlib.pyplot as plt

from ovencontrol import open_sys_id_data as open_data


TEMPERATURE_ORIGIN = 0


def reset_origin(temperature):
    current_origin = np.min(temperature[:5])
    temperature[:] = temperature - (current_origin - TEMPERATURE_ORIGIN)


def plot_signals(ax=None, export=False):
    tests = open_data.retrieve_data_single_inputs(os.path.join('..', 'data', 'system_identification'))
    if ax is None:
        fig, ax = plt.subplots()
    for key in sorted(tests.keys()):
        res = tests[key]
        reset_origin(res.temperature)
        ax.plot(res.time, res.temperature, label=key)
    ax.legend()
    ax.set_ylabel('Temperature increase (deg C)')
    ax.set_xlabel('Seconds since start')
    if export:
        save(fig, filename='tests')


def plot_linearity(export=False):
    tests = open_data.retrieve_data_single_inputs(os.path.join('..', 'data', 'system_identification'))
    fig, ax = plt.subplots()
    for key in sorted(tests.keys()):
        res = tests[key]
        max_output = np.max(res.temperature)
        ax.plot(res.duty_cycle, max_output, 'x', label=key,
                markersize=12, markeredgewidth=2)
    ax.legend()
    ax.set_xlabel('duty cycle')
    ax.set_ylabel('highest temperature')
    ax.set_title('Steady-state gain over input')
    if export:
        save(fig, filename='linearity.png')


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
    plot_signals()
    plot_linearity()
    plt.show()
