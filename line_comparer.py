import re

LINE_THRESHOLDS = {
    "NFL" : .25
}

def convert_bovada_line_to_fraction(line):
    if line == 'EVEN':
        return 1
    elif "-" in line:
        return 100/int(line[1:])
    elif "+" in line:
        return int(line[1:])/100

    raise Exception("Unexpected Line: " + line)

