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


if __name__ == '__main__':
    main()
    plt.show()
