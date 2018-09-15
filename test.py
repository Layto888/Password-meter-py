from password_meter import Password
from constants import *
password = Password('Azerty22')
password.rate()

Password().find(8, display=True, spec=ONLY_PUNCTATIONS + ONLY_DIGITS)
