
MAX_SCORE = 100
MIN_SCORE = 0
MIN_CONSECHAR = 3
MIN_CONSEDIGIT = 2
MIN_SEQUENTIAL = 2
# Minimum length of a password that represents for us a very good score
MIN_LENGTH = 8
# Minimum nb of digits to get the score
MIN_DIGITS = 1
# the min values of lower & upper characters in the password
MIN_LOWUP = 1
# Minimum punctuation
MIN_PUNCT = 2
# we assume there's repetetition when the counter is >= this value.
MIN_REPCHAR = 3
# If the requirement donsn't meet 4/5 of the requierements criteria,
# PLUS + the minimum lenght of password, the score of requirement will be 0.
MIN_REQUIREMENTS = 4
MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 32
MAX_TEST = 50000

# Spec: constant to let user choose what he want include or exclude.
ALL = 0
ONLY_LETTERS = 5
ONLY_DIGITS = 7
ONLY_PUNCTATIONS = 8
# (same as calling ONLY_LETTERS + ONLY_DIGITS)
LETTERS_DIGITS = 12
LETTERS_PONCTUATIONS = 13
DIGITS_PONCTUATIONS = 15