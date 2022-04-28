# -*- coding: utf-8 -*-

def get_temp(first_elem):
    invalid = False
    multiply = 1.00
    current_temperature_fahrenheit = None
    temp, dew = first_elem.split ('/')

    if len (temp) >= 2 and temp[0] == 'M':
        temp = temp[1:]
        multiply = -1.00

    if len (temp) == 2 and temp[0].isdigit () and temp[1].isdigit ():
        temp = float (temp) * (multiply)
        current_temperature_fahrenheit = (temp * 1.8) + 32
    else:
        invalid = True

    if len (dew) >= 2 and dew[0] == 'M':  # dew data if need
        dew = dew[1:]
    if len (dew) == 2 and dew[0].isdigit () and dew[1].isdigit ():
        pass
    else:
        invalid = True
    if not invalid:
        return f"{temp:.2f} C ({current_temperature_fahrenheit:.2f} F)"
    else:
        return "Unknown"


def get_wind(first_elem):
    if 'Z' in first_elem:  # data error correction
        first_elem = first_elem[first_elem.index ('Z') + 1:]

    for idx, i in enumerate (first_elem):
        if i.isdigit ():
            first_elem = first_elem[idx:]
            break

    if first_elem[0].isdigit () and first_elem[1].isdigit () and first_elem[2].isdigit ():
        direction = int (first_elem[0:3])
        first_elem = first_elem[3:]
    else:
        direction = "Unknown"

    G_index = first_elem.find ('G')
    if G_index != -1:
        t = f" at a sustained speed of {int (first_elem[:G_index])} knots"
        gusts = ' gusts'
    else:
        t = ''
        G_index = -1
        gusts = ''

    if first_elem.find ('K') > G_index + 1 and first_elem[G_index + 1:first_elem.find ('K')]:
        first_elem = first_elem[G_index + 1:first_elem.find ('K')]

    if first_elem:
        try:
            knots = int (first_elem)
        except:
            knots = 'Unknown'
    else:
        knots = 'Unknown'
    return f"The wind is blowing from {direction} degrees (true){t} with {knots} knot{gusts}."