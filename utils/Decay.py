__author__ = 'vidi'

from math import exp, log, pow

def decay(delta):
    return pow(0.95, int(delta/30))
