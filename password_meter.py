"""
Password Meter:

github.com/Layto888/Password-meter-py

Compute passwords strength and find the best password.
Rate your password or generate a strong one.

Disclaimer:
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


Nota bene : The program is inspired from :
http://www.passwordmeter.com/ with different approach and proper code.

Features:
    - A simple to use API for testing the strength of your password.
    - Generating strong passwords


Usage example 1:
>>> from password_meter import Password
>>> pas = Password('Azerty22')
>>> pas.show_summary()

Usage example 2:
>>> from password_meter import Password
>>> pas = Password()
>>> pas.find_safe_password(6)
"""

import string
import random
import logging
from constants import *

__author__ = 'A.Amine'
__version__ = '0.1'

# TODO : improve the algo of repetitive_chars() function.
# TODO: add property's for some stuffs.

logger = logging.getLogger('password')
logging.basicConfig(level=logging.WARNING)


class Password(object):
    """ Rate your password or generate a strong one """

    # test array avoid including string.whitespace when generating random
    # passwords.
    test_array = string.ascii_letters + string.punctuation + string.digits

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

    def middle_ns(self):
        """ compute the flat middle numbers or symbols in string. """
        score = 0
        for i, n in enumerate(self.password):
            if i > 0 and i < self.len - 1:
                if n.isdigit() or n in string.punctuation:
                    score += 1
        return 2 * score

    def compute_addition(self):
        """ A) addition part  """
        if self.len < MIN_LENGTH or self.requirement < MIN_REQUIREMENTS:
            self.requirement_factor = 0  # KO
        else:
            self.requirement_factor = 1  # OK

        # adding flat :
        self.score += (self.requirement * 2) * \
            self.requirement_factor + (self.len * 4) + (self.symbol * 6)
        self.score += self.middle_ns()
        # adding cond :
        if self.nupper:
            self.score += (self.len - self.nupper) * 2
        if self.nlower:
            self.score += (self.len - self.nlower) * 2
        if self.ndigit:
            self.score += self.ndigit * 4

    def compute_deduction(self):
        """ B) compute the score of deduction part. """
        self.score += self.only_letters()
        self.score += self.only_digits()
        self.score += self.repetitive_chars2()
        self.score += self.consecutive_letter()
        self.score += self.consecutive_digit()
        self.score += self.check_sequential()

    def only_letters(self):
        if (self.nlower + self.nupper) == self.len:
            return -self.len
        return 0

    def only_digits(self):
        if self.ndigit == self.len:
            return -self.len
        return 0

    # def repetitive_chars(self):
    #     """ If the number of repetition of some 'character' is >= MIN_REPCHAR
    #             we add it to the negative score. """
    #     this_score = 0
    #     occurence = set(self.password)

    #     for letter in occurence:
    #         x = self.password.count(letter)

    #         if x >= MIN_REPCHAR:
    #             this_score += (x ** 2)
    #             logger.debug(

    #                 'letter {} repeated {} x**2 = {}'.format(letter, x, x**2)
    #             )
    #         else:
    #             this_score -= (x * 2)
    #             x = 0

    #     return -this_score

    def repetitive_chars2(self):
        """ If the number of repetition of some 'character' is >= MIN_REPCHAR
                we add it to the negative score """
        cp = 0
        score = 0
        for i in range(0, self.len - 1):
            # check for ascending sequential characters & numbers
            if self.password[i] == self.password[i + 1]:
                cp += 1
            else:
                if cp >= MIN_REPCHAR:
                    logger.info('repetition {}'.format(cp))
                    score += (cp * cp)
                cp = 0
        return - score

    def consecutive_letter(self):
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

    def consecutive_digit(self):
        """ Consecutive numbers, we start the count after the MIN_CONSEDIGIT
        Nota bene: that functions  consecutive_letter and consecutive_digit are
        computed as one score (the consecutive score value) but combined as one
        fucntion, we just split them for more reading readability of code.
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

    def check_sequential(self):
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

    def global_score(self):
        """
        Compute the final score = addition score A + deduction score B
        (see: functions part A / part B).
        """
        self.compute_addition()
        self.compute_deduction()
        self.super_score = self.score - 100
        if self.score > MAX_SCORE:
            self.score = MAX_SCORE
        elif self.score < MIN_SCORE:
            self.score = MIN_SCORE

    def rate_password(self):
        """ This is the function to call if you want rate your password. """
        self.global_score()
        self.show_summary()

    def show_little_summary(self):
        """ Display password and its score each time we find a new
        best password"""
        print('Best password found: {}  Global score {} %  (Ratio {}) '.format
              (
                  self.password, self.score, self.super_score)
              )

    @staticmethod
    def create_random_word(len):
        """generate new Password instance with a random word:
        len is the length. """
        word = ''
        for _ in range(len):
            word += random.choice(Password.test_array)
        return Password(word)

    def find_safe_password(self, length, little_display=True):
        """ This function is to call if yo want find the best password
        with (length l):
        the idea is to generate MAX_TEST of passwords and find the best score.
        """
        assert length >= MIN_PASSWORD_LENGTH, 'Too short for a password.'

        best_password = Password()

        for _ in range(MAX_TEST):
            new_pass = self.create_random_word(length)
            new_pass.global_score()
            if new_pass.score > best_password.score:
                best_password = new_pass
                if little_display:
                    new_pass.show_little_summary()

        # show the best pass found
        best_password.show_summary()

    def show_summary(self):
        """ Display all stuffs about the password"""

        print('\n========= Summary ========= \n')
        print('password: {} '.format(self.password))
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
        print('middle num/symb bonus: {}'.format(self.middle_ns()))
        print('requierements: ({}/5) Bonus {}'.format
              (
                  self.requirement,
                  self.requirement * 2 * self.requirement_factor)
              )
        print('only letters bonus: {}'.format(self.only_letters()))
        print('only digits bonus: {}'.format(self.only_digits()))
        print('repeat chars bonus: {}'.format(self.repetitive_chars2()))
        print('consecutive letters: {}'.format(self.consecutive_letter()))
        print('consecutive digits: {}'.format(self.consecutive_digit()))
        print('sequential (Letters/Digits/Symbols) bonus: {}'.format
              (
                  self.check_sequential())
              )
        print('Your global score: {} %'.format(self.score))
