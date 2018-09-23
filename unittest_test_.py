import password_meter as pm
import unittest


class test_password_meter(unittest.TestCase):
    """class to test the password meter """

    def setUp(self):
        self.pswd = pm.Password(':abcdX01J!b#')

    def testAttributes(self):
        self.assertIsInstance(self.pswd, pm.Password,
                              msg="Isn't an instance of Password class")

        self.assertEqual(self.pswd.password, ':abcdX01J!b#')
        self.assertEqual(self.pswd.len, 12)
        self.assertEqual(self.pswd.nupper, 2)
        self.assertEqual(self.pswd.nlower, 5)
        self.assertEqual(self.pswd.ndigit, 2)
        self.assertEqual(self.pswd.symbol, 3)
        self.assertEqual(self.pswd.requirement, 5)

    def test_middle_ns(self):
        self.assertEqual(self.pswd._middle_ns() / 2, 3)

    def test_only_letters(self):
        self.assertEqual(self.pswd._only_letters(), 0)

    def test_only_digits(self):
        self.assertEqual(self.pswd._only_digits(), 0)

    def test_consecutive_letter(self):
        self.assertEqual(self.pswd._consecutive_letter() / -2, 3)

    def test_consecutive_digit(self):
        self.assertEqual(self.pswd._consecutive_digit() / -2, 1)

    def test_check_sequential(self):
        self.assertEqual(self.pswd._check_sequential() / -3, 2)

    def test_global_score(self):
        self.pswd._global_score()
        self.assertEqual(self.pswd.score, 100)

    def test_random_password(len):
        pass

    def test_specials_cases_password(self):

        # empty password
        self.paswd2 = pm.Password('')

        self.assertEqual(self.paswd2.password, '')
        self.assertEqual(self.paswd2.len, 0)
        self.assertEqual(self.paswd2.nupper, 0)
        self.assertEqual(self.paswd2.nlower, 0)
        self.assertEqual(self.paswd2.ndigit, 0)
        self.assertEqual(self.paswd2.symbol, 0)
        self.assertEqual(self.paswd2.requirement, 0)
        self.paswd2._compute_addition()
        self.assertEqual(self.paswd2.score, 0)
        self.paswd2._compute_deduction()
        self.assertEqual(self.paswd2.score, 0)

        # only digits
        self.paswd2 = pm.Password('0123456789')
        self.assertEqual(self.paswd2._only_digits(), -10.0)
        self.assertEqual(self.paswd2._consecutive_digit(), -18.0)
        self.assertEqual(self.paswd2._check_sequential(), -24.0)

        # only letters
        self.paswd2 = pm.Password('ABCDefcbAARk')
        self.assertEqual(self.paswd2._only_letters(), - 12.0)
        self.assertEqual(self.paswd2._consecutive_letter(), -20.0)
        self.assertEqual(self.paswd2._check_sequential(), -6.0)

    def test_repetitive_chars2(self):
        """ test complexe function _repetitive_chars2 """
        self.paswd2 = pm.Password('axbxcxdxexfx')
        self.assertEqual(self.paswd2._repetitive_chars2(), 0)
        self.paswd2 = pm.Password('abbbbb01b')
        self.assertEqual(self.paswd2._repetitive_chars2(), -16)
        self.paswd2 = pm.Password('000000013xbv11')
        self.assertEqual(self.paswd2._repetitive_chars2(), -37)
        self.paswd2 = pm.Password('Oharrrrrrrrrrrrrrrrg!')
        self.assertEqual(self.paswd2._repetitive_chars2(), -100)


if __name__ == "__main__":
    unittest.main()
