import os
import csv
import numpy as np


class TestResults:
    def __init__(self):
        self.pulse_width = None  # ms
        self.duty_cycle = None   # ratio, 0 -- 1. Single value or array.
        self.time = None
        self.temperature = None


def parse_row(row):
    var1 = float(row[0])
    if row[1] == 'N/A':
        var2 = np.nan
    else:
        var2 = float(row[1])
    return var1, var2


def check_header_row(row, str1, str2):
    assert str1 in row[0]
    assert str2 in row[1]


def process_csv(filepath):
    time = []
    temperature = []
    test_results = TestResults()
    with open(filepath) as f:
        reader = csv.reader(f)
        next(reader)  # skip the first PuTTY row
        check_header_row(next(reader), 'pulseWidth', 'dutyCycle')
        pulse_width, duty_cycle = parse_row(next(reader))
        if np.isnan(duty_cycle):
            duty_cycle = []
        check_header_row(next(reader), 'time', 'temperature')
        for i, row in enumerate(reader):
            res = parse_row(row)
            time.append(res[0])
            temperature.append(res[1])
            if len(res) > 2:
                duty_cycle.append(res[2])
    test_results.pulse_width = pulse_width
    test_results.duty_cycle = np.array(duty_cycle) if type(duty_cycle) is list else duty_cycle
    test_results.time = np.array(time)
    test_results.temperature = np.array(temperature)
    return test_results


def retrieve_data(path):
    res = {}
    test_random = None
    for filename in os.listdir(path):
        if not filename.endswith('.csv'):
            continue
        test_results = process_csv(os.path.join(path, filename))
        if type(test_results.duty_cycle) is float:
            res[test_results.duty_cycle] = test_results
        else:
            test_random = test_results
    return res, test_random

