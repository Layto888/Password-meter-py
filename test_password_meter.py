from password_meter import Password
import pytest


# set up fixture
@pytest.fixture(scope='module')
def password():
    pswd = Password(':abcdX01J!b#')
    yield pswd


def test_attributes(password):
    assert isinstance(password, Password())
    assert isinstance(password.password, str)
