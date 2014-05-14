__author__ = 'vidi'
from math import exp, log, pow

SIG = 15
MU = 0


def gaussian(value, distance):
    SIG = 10
    return value * exp(-pow(distance, 2.) / (2 * pow(SIG, 2.)))


def decay_gaussian(mu, day):
    SIG = 20
    return 0.02 * exp(-pow(day-mu, 2.) / (2 * pow(SIG, 2.)))