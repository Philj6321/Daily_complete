""" elcalc.py -- simplistic electrical calculator

Python warm-up exercise for TPRG 2131 intro week 1-2

Determine the type of calculation: total resistance, resistor-capacitor or
series RLC.
If resistance, prompt for series or parallel resistance, then prompt for
resistors 1 and 2, output the total resistance according to the response.
If resistance-capacitance, prompt for resistor and capacitor, then output
RC product.
If RLC, prompt for capacitor and inductor and calculate series resonant
centre frequency, bandwidth and Q factor.
The values are entered as SI units: Ohm, Farad, Henry. For example,
1k0 is 1000 or 1.0e3 and 1uF is 0.000001 or 1.0e-6
Additional checks:
 - Values entered are non-zero positive.
 - Quits gracefully if the user chooses "q" or "Q" but CTRL-C still works
   to crash out.
"""

from math import pi, sqrt

def prompt_for_positive_value(message):
    """Prompt for float value, persist until value > 0.
message is the prompt that is sent out verbatim."""
    value = float(input(message + " "))
    while value <= 0.0:
        value = float(input("The value must be greater than zero\n"
                        + message + " "))
    return value

def prompt_for_option_2(message, answer1, answer2):
    """Prompt for one of two option codes, persist until valid choice.
message is the prompt that is sent out verbatim.
answer1, answer2 are expected input strings, typically single letters
but not necessarily so."""
    response = input(message + " ")
    while response != answer1 and response != answer2:
        response = input("Please respond with one of the two options.\n"
                        + message + " ")
    return response
    
def prompt_for_options(message, answers):
    """Prompt for one of list of option codes, persist until valid choice.
message is the prompt that is sent out verbatim.
answers is a list of expected input strings, typically single letters
but not necessarily so."""
    response = input(message + " ")
    while True:
        # Loop until the response matches one of the choice strings.
        for ans in answers:
            if response == ans:
                return response
        response = input("Please respond with one of the options.\n"
                            + message + " ")

def series_resonance(inductor, capacitor):
    """Centre frequency at resonance of a series RLC circuit (float).
    inductor is the inductance in Henries (e.g. 22mH would be 0.022H)
    capacitor is the capacitance in Farads (e.g. 33uF would be 0.000033F)."""
    return 1.0 / (2.0 * pi * sqrt(inductor * capacitor))

def series_bandwidth(inductor, resistor):
    """Bandwidth of the resonant series RLC circuit (float).
    inductor is the inductance in Henries (e.g. 22mH would be 0.022H)
    resistor is the resistance in Ohms."""
    return resistor / (2.0 * pi * inductor)

def series_q_factor(inductor, capacitor, resistor):
    """Q factor of the resonant series RLC circuit (float).
    inductor is the inductance in Henries (e.g. 22mH would be 0.022H)
    capacitor is the capacitance in Farads (e.g. 33uF would be 0.000033F)
    resistor is the resistance value in Ohms."""
    return sqrt(inductor / capacitor) / resistor

############
### Main ###
############
print("Electrical circuit calculator\n(CTRL-C to quit)")

while True:
    # Get user's choice
    calc_type = prompt_for_options(
        """\nCalculate
(1) total resistance
(2) RC time constant
(3) Series RLC parameters
(Q) Quit program
> """,
        ("1", "2", "3", "q", "Q"))

    if calc_type == "q" or calc_type == "Q":  # program ends
        break

    elif calc_type == "1":
        # Get user's choice
        choice = prompt_for_option_2("Calculate series (1) or parallel (2)?",
                                     "1", "2")
        # Resistance calculation
        res1 = prompt_for_positive_value("What is resistance 1 in ohms?")
        res2 = prompt_for_positive_value("What is resistance 2 in ohms?")
        # Calculate the total resistance
        if choice == "1":
            res_total = res1 + res2
            print("Series R: {:.3g}\u2126 + {:.3g}\u2126 = {:.3g}\u2126"
                  .format(res1, res2, res_total))
        elif choice == "2":
            res_total = 1.0 / (1.0/res1 + 1.0/res2)
            print("Parallel R: {:.3g}\u2126 // {:.3g}\u2126 = {:.3g}\u2126"
                  .format(res1, res2, res_total))
        else:
            print("Invalid choice, nothing calculated")  # should never happen!

    elif calc_type == "2":
        # RC time constant calculation
        res = prompt_for_positive_value("What is the resistance in ohms?")
        cap = prompt_for_positive_value("What is the capacitance in farads?")
        tau = res * cap;
        print("RC time constant:", res, cap, tau)

    elif calc_type == "3":
        # RC time constant calculation
        res = prompt_for_positive_value("What is the resistance in ohms?")
        cap = prompt_for_positive_value("What is the capacitance in farads?")
        ind = prompt_for_positive_value("What is the inductance in henries?")
        freq = series_resonance(ind, cap);
        bandwidth = series_bandwidth(ind, res)
        qfactor = series_q_factor(ind, cap, res)
        print("RLC circuit elements: {:.3g}F, {:.3g}H, {:.1f}\u2126".format(cap, ind, res))
        print("Centre frequency: {:.3g}Hz".format(freq))
        print("Series bandwidth: {:.3g}Hz".format(bandwidth))
        print("Series Q factor: {:.3g}".format(qfactor))

    else:
        print("Invalid choice, nothing calculated")  # should never happen!

print("Done!")
