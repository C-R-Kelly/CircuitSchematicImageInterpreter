# -*- coding: utf-8 -*-
"""
Component List
==============

List of all possible components, their OCR value and their number of terminals

author: C. R. Kelly
email: CK598@cam.ac.uk

"""
def getComponents():
# component name, OCR Value, Number of Terminals
    COMPONENT_LIST = [
        ('Capacitor',                           '0',  2),
        ('Resistor (EU)',                       '1',  2),
        ('Thermistor (EU)',                     '2',  2),
        ('Diode',                               '3',  2),
        ('Voltmeter',                           '4',  2),
        ('Ammeter',                             '5',  2),
        ('Light Bulb',                          '6',  2),
        ('Motor',                               '7',  2),
        ('LDR (EU)',                            '8',  2),
        ('LED',                                 '9',  2),
        ('Cell',                                '@',  2),
        ('Potentiometer (EU)',                  '[',  3),
        ('Variable Resistor (EU)',              ']',  2),
        ('Resistor (US)',                       '+',  2),
        ('Thermistor (US)',                     '-',  2),
        ('LDR (US)',                            '*',  2),
        ('Potentiometer (US)',                  '{',  3),
        ('Variable Resistor (US)',              '}',  2),
        ('Open Switch',                         '<',  2),
        ('Closed Switch',                       '>',  2),
        ('Relay 1',                             '\\', 3),
        ('Relay 2',                             '/',  3),
        ('NPN Transistor',                      'A',  3),
        ('PNP Transistor',                      'a',  3),
        ('MOSFET',                              '(',  3),
        ('Inductor',                            ')',  2),
        ('NULL - CHECK DATA',                 '\x0c', 0),
    ]

    return COMPONENT_LIST
