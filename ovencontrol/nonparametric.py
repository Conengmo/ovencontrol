import os
import numpy as np
import matplotlib.pyplot as plt

from ovencontrol import open_data


def main():
    res = open_data.retrieve_data_random_input(os.path.join('..', 'data'))
    fig, axs = plt.subplots(2, sharex=True)
    axs[0].plot(res.time, res.temperature)
    axs[1].plot(res.time, res.duty_cycle)
    # ax.legend()
    # ax.set_ylabel('Temperature (deg C)')
    # ax.set_xlabel('Seconds since start')


if __name__ == '__main__':
    main()
    plt.show()
