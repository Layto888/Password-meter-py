from password_meter import Password
from constants import ALL 


password = Password('Alpha20')

password.find(8, display=True, spec=ALL)