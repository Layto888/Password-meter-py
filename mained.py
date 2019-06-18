from password_meter import Password
from constants import *
from matplotlib import pyplot as plt

# find best password algorithm
Password().find(12, spec=ALL, msg='spec=ALL')
Password().find(12, spec=USE_LETTERS + USE_DIGITS, msg='spec=LETTERS + DIGITS')
Password().find(12, spec=USE_LETTERS + USE_PUNCTATIONS, msg='spec=LETTERS + PUNCTATIONS')
Password().find(12, spec=USE_DIGITS + USE_PUNCTATIONS, msg='spec=DIGITS + PUNCTATIONS')

# graph to show passwords safety evolution with a certain number of tries.
Password().drawGraph()
