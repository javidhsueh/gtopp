__author__ = 'vidi'
from math import exp, log, pow

SIG = 4.2
MU = 0


def gaussian(value, distance):
    return value * exp(-pow(distance - MU, 2.) / (2 * pow(SIG, 2.)))


#
# print Gaussian(1, 1)
# print Gaussian(1, 2)
#
# print Gaussian(1, 3)
# print Gaussian(1, 4)
# print Gaussian(1, 5)
#
# print Gaussian(1, 10)
#
