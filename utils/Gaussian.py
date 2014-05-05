__author__ = 'vidi'
from math import exp, log, pow

SIG = 35
MU = 0


def gaussian(value, distance):
    return value * exp(-pow(distance, 2.) / (2 * pow(SIG, 2.)))


# #
# print gaussian(1, 1)
# print gaussian(1, 2)
#
# print gaussian(1, 3)
# print gaussian(1, 4)
# print gaussian(1, 5)
#
# print gaussian(1, 10)
#
