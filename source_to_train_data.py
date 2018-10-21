import csv
import sys

source = csv.reader(sys.stdin)

# use first three lines as source of prediction
line_1 = source.next()
line_2 = source.next()
line_3 = source.next()

result = []

for line in source:
    result += [[line[1]] + line_3[2:5] + line_2[2:5] + line_1[2:5]]
    # shift lines
    line_1 = line_2
    line_2 = line_3
    line_3 = line

writer = csv.writer(sys.stdout)
writer.writerows(result)
