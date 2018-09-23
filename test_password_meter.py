import pytest
from password_meter import Password
from constants import ALL, ONLY_LETTERS, ONLY_DIGITS, ONLY_PUNCTATIONS


# set up fixture
@pytest.fixture(scope='module')
def password():
    pswd = Password(':abcdX01J!b#')
    yield pswd


def test_attributes(password):
    assert isinstance(password, Password)
    assert isinstance(password.password, str)
    assert password.len == 12
    assert password.nupper == 2
    assert password.nlower == 5
    assert password.ndigit == 2
    assert password.symbol == 3
    assert password.requirement == 5


def test_middle_ns(password):
    assert password._middle_ns() / 2 == 3


def test_only_letters(password):
    assert password._only_letters() == 0


def test_only_digits(password):
    assert password._only_digits() == 0


def test_consecutive_letter(password):
    assert password._consecutive_letter() / -2 == 3


def test_consecutive_digit(password):
    assert password._consecutive_digit() / -2 == 1


def test_check_sequential(password):
    assert password._check_sequential() / -3 == 2


def test_global_score(password):
    password._global_score()
    assert password.score == 100


# test specifications types
def test_random_password_spec(password):
    assert ALL == ONLY_LETTERS + ONLY_DIGITS + ONLY_PUNCTATIONS
    # new find safe password test with cases:
    passwd, score = Password().find(8, spec=ONLY_DIGITS)
    assert len(passwd) == 8
    s_digits = sum(c.isdigit() for c in passwd)
    assert s_digits == 8
    passwd, score = Password().find(8, spec=ONLY_LETTERS)
    s_letters = sum(c.isalpha() for c in passwd)
    assert s_letters == 8
    assert score > 5.0 and score < 100.0


# test special cases password
def test_specials_cases_password():
    special_pass = Password('')

    assert special_pass.len == 0
    assert special_pass.nupper == 0
    assert special_pass.nlower == 0
    assert special_pass.ndigit == 0
    assert special_pass.symbol == 0
    assert special_pass.requirement == 0
    # score compute part A and B
    special_pass._compute_addition()
    assert special_pass.score == 0
    special_pass._compute_deduction()
    assert special_pass.score == 0
    special_pass._global_score()
    assert special_pass.score == 0
    # only digits
    special_pass = Password('0123456789')
    assert special_pass._only_digits() == -10.0
    assert special_pass._consecutive_digit() == -18.0
    assert special_pass._check_sequential() == -24.0
    # only letters
    special_pass = Password('ABCDefcbAARk')
    assert special_pass._only_letters() == - 12.0
    assert special_pass._consecutive_letter() == -20.0
    assert special_pass._check_sequential() == -6.0


def test_repetitive_chars2():
    """ test complexe function _repetitive_chars2 """
    passwd = Password('axbxcxdxexfx')
    assert passwd._repetitive_chars2() == 0
    passwd = Password('abbbbb01b')
    assert passwd._repetitive_chars2() == -16
    passwd = Password('000000013xbv11')
    assert passwd._repetitive_chars2() == -37
    passwd = Password('Oharrrrrrrrrrrrrrrrg!')
    assert passwd._repetitive_chars2() == -100
