import os
import csv


def repair_dc02(path):
    """Repair a certain csv file with wrong numbering."""
    with open(os.path.join(path, 'dc0-2.csv')) as f, open(os.path.join(path, 'dc0-2_out.csv'), 'a', newline='') as f_out:
        reader = csv.reader(f)
        writer = csv.writer(f_out)
        offset = None
        for i, row in enumerate(reader):
            if i < 200:
                continue
            t = int(row[0])
            if t == 462:
                if offset is None:
                    offset = i
                writer.writerow([t + 2 * (i - offset), row[1]])


# if __name__ == '__main__':
#     path = os.path.join('..', 'data')
#     repair_dc02(path)
