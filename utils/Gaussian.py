__author__ = 'vidi'
from math import exp, log, pow

SIG = 20
MU = 0


def gaussian(value, distance):
    return value * exp(-pow(distance, 2.) / (2 * pow(SIG, 2.)))
