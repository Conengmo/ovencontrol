import os
import csv
import numpy as np
import matplotlib.pyplot as plt


class TestResults:
    def __init__(self, filename):
        filepath = os.path.join('..', 'data', 'control_test', filename)
        self.time = []
        self.phase = []
        self.setpoint = []
        self.temperature = []
        self.control_input = []
        self.process_csv(filepath)

    def process_csv(self, filepath):
        time_at_phase_start = 0
        with open(filepath) as f:
            reader = csv.reader(f)
            next(reader)  # skip the first PuTTY row
            for i, row in enumerate(reader):
                self.phase.append(int(row[0]))
                if i > 0 and self.phase[-1] != self.phase[-2]:
                    time_at_phase_start = self.time[-1] + 1  # add one second for time between phases
                self.time.append(time_at_phase_start + int(row[1]))
                self.setpoint.append(float(row[2]))
                self.temperature.append(float(row[3]))
                self.control_input.append(float(row[4]))
        self.time = np.array(self.time)
        self.phase = np.array(self.phase)
        self.setpoint = np.array(self.setpoint)
        self.temperature = np.array(self.temperature)
        self.control_input = np.array(self.control_input)


def main():
    filename = 'run1.csv'
    res = TestResults(filename)
    fig, axs = plt.subplots(3, 1, sharex=True, tight_layout=True)
    axs[0].plot(res.time, res.phase, label='phase')
    axs[0].legend()
    axs[1].plot(res.time, res.setpoint, label='setpoint')
    axs[1].plot(res.time, res.temperature, label='temperature')
    axs[1].legend()
    axs[2].plot(res.time, res.control_input, label='input')
    axs[2].legend()


if __name__ == '__main__':
    main()
    plt.show()