[![Build Status](https://travis-ci.org/Layto888/Password-meter-py.svg?branch=master)](https://travis-ci.org/Layto888/Password-meter-py)
# Password-meter-py
* Author: Amine Amardjia.
* https://github.com/Layto888/Password-meter-py

Test the strength of your password or generate a strong one.
Rate your password or generate a strong one.
  
* Disclaimer:

This application is designed to assess the strength of password strings.
And provides the user a means to improvethe strength of their passwords, 
with a hard focus on breaking the typical bad habits of faulty password 
formulation.

Since no official weighting system exists, we created our own formulas
to assess the overall strength of a given password.

Please note, that this application does not utilize the typical "days-to-crack"
approach for strength determination.
We have found that particular system to be severely lacking and unreliable
for real-world scenarios. This application is neither perfect nor foolproof,
and should only be utilized as a loose guide in determining methods for
improving the password creation process

# Features:
- A simple to use API for testing the strength of your password.
- Generating strong passwords.




Usage example 1:
```python
>>> from password_meter import Password
>>> password = Password('Azerty22')
>>> password.rate()
```
Usage example 2:
```python
>>> from password_meter import Password
>>> from constants import *
>>> Password().find(8, display=True, spec=ONLY_PUNCTATIONS+ONLY_DIGITS)
# or:
>>> my_password, my_score = Password().find(8)
 ```
TODO: 
 - [x] add unittest file
 - [x] let user choose if he wants include : digits / symbols ..etc.
 - [x] add password strength infos text.
 - [x] add improvement password suggestion in case of weak password. 
