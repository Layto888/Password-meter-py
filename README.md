# Password-meter-py
Test the strength of your password or generate a strong one.

Password Meter: github.com/Layto888/Password-meter-py

Rate your password or generate a strong one.

Features:
- A simple to use API for testing the strength of your password.
- Generating strong passwords.

```python
>>> from password_meter import Password
>>> pas = Password('Azerty22')
>>> pas.rate_password()
```
Usage example 2:
```python
>>> from password_meter import Password
>>> Password().find_safe_password(7)
# or:
>>> my_password, my_score = pw.find_safe_password(7, display=False)
 ```                   

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
improving the password creation process.

TODO: 
 - [x] add unittest file
 - [ ] rethink the check_sequential() function.
 - [ ] add password strength infos text. 
