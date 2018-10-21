import csv
import sys

def ppm_to_category(ppm):
    result = 0
    if ppm > 300:
        result = 5
    elif ppm > 200:
        result = 4
    elif ppm > 150:
        result = 3
    elif ppm > 100:
        result = 2
    elif ppm > 50:
        result = 1
    return result

source = csv.reader(sys.stdin)

# use first three lines as source of prediction
line_1 = source.next()
line_2 = source.next()
line_3 = source.next()

result = []

for line in source:
    # convert target ppm to category


    result += [[ppm_to_category(int(line[1]))] + line_3[2:5] + line_2[2:5] + line_1[2:5]]
    # shift lines
    line_1 = line_2
    line_2 = line_3
    line_3 = line

writer = csv.writer(sys.stdout)
writer.writerows(result)
