
import string

__author__ = 'A.Amine'
__version__ = '0.1'
__doc__ = 'Rate the strength of passwords'


MAX_SCORE = 100
MIN_SCORE = 0

MIN_CONSECHAR = 2
MIN_CONSEDIGIT = 2
MIN_SEQUENTIAL = 3
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

# TODO : improve the algo of repetitive_chars() function.


class Password(object):
    def __init__(self, password):
        self.password = password
        self.len = 0
        self.nupper = 0
        self.nlower = 0
        self.ndigit = 0
        self.symbol = 0
        self.requirement = 0
        self.score = 0.0  # limited [0% - 100%]
        self.super_score = 0.0  # the real score
        self.requirement_factor = 0
        self._get_infos()

    def __repr__(self):
        return str(self.__dict__)

    def _get_infos(self):

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

        """ alors the fucntion check for default minimum requirements
        by incrementing self.requirement for each case bellow:
        - Minimum  MIN_LENGTH characters in length
        - Contains 3/4 of the following items + the min length.:
        - Uppercase Letters  MIN_LOWUP
        - Lowercase Letters MIN_LOWUP
        - Numbers MIN_DIGITS
        - Symbols  MIN_PUNCT """

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
        """ B) compute the score of deduction part """
        self.score += self.only_letters()
        self.score += self.only_digits()
        self.score += self.repetitive_chars()
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

    def repetitive_chars(self):
        """ If the number of repetition of some 'character' is >= MIN_REPCHAR
                we add it to the negative score """
        this_score = 0
        occurence = set(self.password)

        for letter in occurence:
            x = self.password.count(letter)
            if x >= MIN_REPCHAR:
                this_score += (x ** 2)
            else:
                this_score -= (x * 2)

        return -this_score

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
        """This is the function to call outside the class
        to compute the final score = addition score A + deduction score B
        (see: functions part A / part B).
        """
        self.compute_addition()
        self.compute_deduction()
        self.super_score = self.score
        if self.score > MAX_SCORE:
            self.score = MAX_SCORE
        elif self.score < MIN_SCORE:
            self.score = MIN_SCORE

    def show_summary(self):
        """ Display all stuffs about the password"""

        print('\n========= Summary ========= \n')
        print('password: {} '.format(self.password))
        print('length: {} Bonus {}'.format(self.len, self.len * 4))
        if self.nupper > 0:
            print('Upper Letters: {} Bonus {}'.format(
                self.nupper, (self.len - self.nupper) * 2))
        else:
            print('upper Letters: {} Bonus {}'.format(self.nupper, 0))
        if self.nlower > 0:
            print('lower Letters: {} Bonus {}'.format(
                self.nlower, (self.len - self.nlower) * 2))
        else:
            print('lower Letters: {} Bonus {}'.format(self.nlower, 0))
        print('numbers: {} Bonus {}'.format(self.ndigit, self.ndigit * 4))
        print('symbols: {} Bonus {}'.format(self.symbol, self.symbol * 6))
        print('middle Num/Symb Bonus: {}'.format(self.middle_ns()))
        print('Requierements: {}/5 Bonus {}'.format
              (
                  self.requirement,
                  self.requirement * 2 * self.requirement_factor)
              )

        print('only Letters Bonus: {}'.format(self.only_letters()))
        print('only Digits Bonus: {}'.format(self.only_digits()))
        print('repeat Chars Bonus: {}'.format(self.repetitive_chars()))
        print('consecutive Letters: {}'.format(self.consecutive_letter()))
        print('consecutive Digits: {}'.format(self.consecutive_digit()))
        print('sequential (Letters/Digits/Symbols) Bonus: {}'.format
              (
                  self.check_sequential())
              )
        print('Your global score: {} %'.format(self.score))


pas = Password('Bq18987654')
print(pas)
pas.global_score()
pas.show_summary()


input()
