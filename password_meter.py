"""
Password Meter:github.com/Layto888/Password-meter-py

Compute passwords strength and find the best password.
Rate your password or generate a strong one.

Disclaimer:
This application is designed to assess the strength of password strings.
The instantaneous visual feedback provides the user a means to improve
the strength of their passwords, with a hard focus on breaking the
typical bad habits of faulty password formulation.

Since no official weighting system exists, we created our own formulas
to assess the overall strength of a given password.

Please note, that this application does not utilize the typical "days-to-crack"
approach for strength determination.
We have found that particular system to be severely lacking and unreliable
for real-world scenarios. This application is neither perfect nor foolproof,
and should only be utilized as a loose guide in determining methods for
improving the password creation process.

Nota bene: The program is inspired from :
http://www.passwordmeter.com/ with different approach and proper code.

Features:
    - A simple to use API for testing the strength of your password.
    - Generating strong passwords
    - suggest improvement in case of weak password.


Usage example 1:
>>> from password_meter import Password
>>> password = Password('Azerty22')
>>> password.rate()

Usage example 2:
>>> from password_meter import Password
>>> from constants import * 
>>> Password().find(8, display=True, spec=ONLY_PUNCTATIONS+ONLY_DIGITS)
"""

import string
import random
import logging
from constants import *

__author__ = 'A.Amine'
__version__ = '0.4'

logger = logging.getLogger('password')
logging.basicConfig(level=logging.WARNING)


class Password(object):
    """ Rate your password or generate a strong one """

    # test array avoid including string.whitespace when generating random
    # passwords.
    str_array = string.ascii_letters
    pnc_array = string.punctuation
    dgt_array = string.digits
    global_array = str_array + pnc_array + dgt_array

    def __init__(self, password=''):

        self.password = password
        self.len = 0
        self.nupper = 0
        self.nlower = 0
        self.ndigit = 0
        self.symbol = 0
        self.requirement = 0
        self.score = 0.0  # limited [0% - 100%]
        self.super_score = 0.0  # the real score - 100 %
        self.requirement_factor = 0
        self._get_infos()

    def find(self, length, display=False, spec=ALL):
        """ This function is to call if yo want find the best password
        with (length l):
        the idea is to generate MAX_TEST of passwords and find the best score.
        return the safest password.
        use spec to specify if you want to includes: letters, digits, symbols.
        """
        assert (length >= MIN_PASSWORD_LENGTH), 'Insufficient length for a password'
        assert (length <= MAX_PASSWORD_LENGTH), 'Length too large for a password'
        # check for spec
        if spec > ALL:
            logger.error('\nThis specification is not allowed. -> set spec to default.\n')
            spec = ALL

        best_password = Password()

        for _ in range(MAX_TEST):
            new_pass = self._random_password(length, spec)
            new_pass._global_score()
            if new_pass.score > best_password.score:
                best_password = new_pass
                if display:
                    new_pass._show_little_summary()
        # show the best pass found
        if display:
            best_password._show_summary()
        return best_password.password, best_password.score

    def rate(self):
        """
        This is the function to call if you want rate your password.
        return: the score value.
        """
        self._global_score()
        self._show_summary()
        self._suggest_improvement()
        return self.score

    def _suggest_improvement(self):
        """
        If the score is under 50% it will be considered 'weak'
        suggest then some improvement depending on the original password letters.
        """
        if self.score < MAX_SCORE / 2.0:
            additional_part, score = self.find(MIN_LENGTH - 2, spec=ONLY_DIGITS + ONLY_PUNCTATIONS)
            improved_password = self.password + additional_part
            print('\nYour password is pretty weak, we suggest: {}'.format(improved_password))

    def __repr__(self):
        return str(self.__dict__)

    def _get_infos(self):
        """ alors the fucntion compute lower/uper/digit...and check for default
        minimum requirements by incrementing self.requirement for each
        case bellow:
        - Minimum  MIN_LENGTH characters in length
        - Contains 3/4 of the following items + the min length.:
        - Uppercase Letters  MIN_LOWUP
        - Lowercase Letters MIN_LOWUP
        - Numbers MIN_DIGITS
        - Symbols  MIN_PUNCT """

        for letter in self.password:
            if letter.isupper():
                self.nupper += 1
            elif letter.islower():
                self.nlower += 1
            elif letter.isdigit():
                self.ndigit += 1
            elif letter in string.punctuation:
                self.symbol += 1

        self.len = len(self.password)

        if self.len > MIN_LENGTH:
            self.requirement += 1
        if self.ndigit > MIN_DIGITS:
            self.requirement += 1
        if self.nlower > MIN_LOWUP:
            self.requirement += 1
        if self.nupper > MIN_LOWUP:
            self.requirement += 1
        if self.symbol > MIN_PUNCT:
            self.requirement += 1
        logger.info('total self.requirement = {}'.format(self.requirement))

    def _middle_ns(self):
        """ compute the flat middle numbers or symbols in string. """
        score = 0
        for i, n in enumerate(self.password):
            if i > 0 and i < self.len - 1:
                if n.isdigit() or n in string.punctuation:
                    score += 1
        return 2 * score

    def _compute_addition(self):
        """ A) addition part  """
        if self.len < MIN_LENGTH or self.requirement < MIN_REQUIREMENTS:
            self.requirement_factor = 0  # KO
        else:
            self.requirement_factor = 1  # OK

        # adding flat :
        self.score += (self.requirement * 2) * \
            self.requirement_factor + (self.len * 4) + (self.symbol * 6)
        self.score += self._middle_ns()
        # adding cond :
        if self.nupper:
            self.score += (self.len - self.nupper) * 2
        if self.nlower:
            self.score += (self.len - self.nlower) * 2
        if self.ndigit:
            self.score += self.ndigit * 4

    def _compute_deduction(self):
        """ B) compute the score of deduction part. """
        self.score += self._only_letters()
        self.score += self._only_digits()
        self.score += self._repetitive_chars2()
        self.score += self._consecutive_letter()
        self.score += self._consecutive_digit()
        self.score += self._check_sequential()

    def _only_letters(self):
        if (self.nlower + self.nupper) == self.len:
            return -self.len
        return 0

    def _only_digits(self):
        if self.ndigit == self.len:
            return -self.len
        return 0

    def _repetitive_chars2(self):
        """ Each time the number of repetition of some 'character' is >= MIN_REPCHAR
                we add its square to the negative score """
        cp = 0
        score = 0
        rep_array = []

        for i in range(0, self.len - 1):
            # check for ascending sequential characters & numbers
            if self.password[i] == self.password[i + 1]:
                cp += 1
            else:
                if cp >= MIN_REPCHAR:
                    rep_array.append(cp)
                    logger.info('add to rep_array: {}'.format(cp))
                    cp = 0

        rep_array.append(cp)
        for value in rep_array:
            score += (value * value)
        if score > MAX_SCORE:
            score = MAX_SCORE
            score = MAX_SCORE
        return - score

    def _consecutive_letter(self):
        """ Consecutive Uppercase letters and lower (case insensitive)
            we start the count after the 'MIN_CONSECHAR=2' consecutive
            character in the string. """
        score = 0
        cp = 0
        for letter in self.password:
            if letter.isalpha():
                cp += 1
                if cp >= MIN_CONSECHAR:
                    score += 1
                    logger.info('consec letter {}:{} time >= {} '.format
                                (
                                    score, cp, MIN_CONSECHAR)
                                )
            else:
                cp = 0
        return -2 * score

    def _consecutive_digit(self):
        """ Consecutive numbers, we start the count after the MIN_CONSEDIGIT
        Nota bene: that functions  consecutive_letter and consecutive_digit are
        computed as a single score (the consecutive score value), combined as one
        fucntion, we just split them for more readability.
        """
        score = 0
        cp = 0
        for letter in self.password:
            if letter.isdigit():
                cp += 1
                if cp >= MIN_CONSEDIGIT:
                    score += 1
                    logger.info('consec digit {} time >= {} '.format
                                (
                                    cp, MIN_CONSECHAR)
                                )
            else:
                cp = 0
        return -2 * score

    def _check_sequential(self):
        """ check for ascending/descending sequential Letters & digits;
        start when the counter is >= MIN_SEQUENTIAL """
        score = 0
        cp_asc_seq = cp_des_seq = 0

        for i in range(0, self.len - 1):
            # check for ascending sequential characters & numbers
            if ord(self.password[i]) + 1 == ord(self.password[i + 1]):
                cp_asc_seq += 1
                if cp_asc_seq >= MIN_SEQUENTIAL:
                    score += 1

            # check for descending sequential characters & numbers
            elif ord(self.password[i]) == ord(self.password[i + 1]) + 1:
                cp_des_seq += 1
                if cp_des_seq >= MIN_SEQUENTIAL:
                    score += 1
            else:
                cp_asc_seq = cp_des_seq = 0

        return -3 * score

    def _global_score(self):
        """
        Compute the final score = addition score A + deduction score B
        (see: functions part A / part B).
        """
        self._compute_addition()
        self._compute_deduction()
        self.super_score = self.score - 100
        if self.score > MAX_SCORE:
            self.score = MAX_SCORE
        elif self.score < MIN_SCORE:
            self.score = MIN_SCORE

    def _show_little_summary(self):
        """ Display password and its score each time we find a new
        best password"""
        print('Best password found: {}  Global score {} %  (Ratio {}) '.format
              (
                  self.password, self.score, self.super_score)
              )

    @staticmethod
    def _random_password(len, spec=ALL):
        """generate new Password instance with a random word:
        len is the length.
        """
        if spec == ALL:
            list_char = Password.global_array
        elif spec == ONLY_LETTERS:
            list_char = Password.str_array
        elif spec == ONLY_DIGITS:
            list_char = Password.dgt_array
        elif spec == ONLY_PUNCTATIONS:
            list_char = Password.pnc_array
        elif spec == ONLY_LETTERS + ONLY_DIGITS:
            list_char = Password.str_array + Password.dgt_array
        elif spec == ONLY_LETTERS + ONLY_PUNCTATIONS:
            list_char = Password.str_array + Password.pnc_array
        elif spec == ONLY_DIGITS + ONLY_PUNCTATIONS:
            list_char = Password.pnc_array + Password.dgt_array

        word = ''
        for _ in range(len):
            word += random.choice(list_char)
        return Password(word)

    def _show_summary(self):
        """ Display all stuffs about the password"""

        print('\n========= Summary ========= \n')
        print('password: {} \n'.format(self.password))
        print('length: ({}) Bonus {}'.format(self.len, self.len * 4))

        if self.nupper > 0:
            print('upper letters: ({}) Bonus {}'.format
                  (
                      self.nupper, (self.len - self.nupper) * 2)
                  )
        else:
            print('upper letters: ({}) Bonus {}'.format(self.nupper, 0))

        if self.nlower > 0:
            print('lower letters: ({}) Bonus {}'.format
                  (
                      self.nlower, (self.len - self.nlower) * 2)
                  )
        else:
            print('lower letters: ({}) Bonus {}'.format(self.nlower, 0))

        print('numbers: ({}) Bonus {}'.format(self.ndigit, self.ndigit * 4))
        print('symbols: ({}) Bonus {}'.format(self.symbol, self.symbol * 6))
        print('middle num/symb bonus: {}'.format(self._middle_ns()))
        print('requierements: ({}/5) Bonus {}'.format
              (
                  self.requirement,
                  self.requirement * 2 * self.requirement_factor)
              )
        print('only letters bonus: {}'.format(self._only_letters()))
        print('only digits bonus: {}'.format(self._only_digits()))
        print('repeat chars bonus: {}'.format(self._repetitive_chars2()))
        print('consecutive letters: {}'.format(self._consecutive_letter()))
        print('consecutive digits: {}'.format(self._consecutive_digit()))
        print('sequential (Letters/Digits/Symbols) bonus: {}'.format
              (
                  self._check_sequential())
              )
        print('Your global score: {} %'.format(self.score))
