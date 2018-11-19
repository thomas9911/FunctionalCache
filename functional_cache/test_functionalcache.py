import pytest
from functional_cache import FunctionalCache
from unittest.mock import ANY
from unittest import mock


@pytest.fixture(scope='module')
def functionalcaches():
    f = FunctionalCache()
    return f


def test_wrapped_function_puts_answer_in_db(functionalcaches):
    @functionalcaches.cache
    def testtest(a, b):
        return a + b

    with mock.patch.object(functionalcaches, 'apply_function',
                           wraps=functionalcaches.apply_function) as monkey:
        assert 2 == testtest(1, 1)
        monkey.assert_called_with(ANY, 'testtest', (1, 1), {})


def test_function_output_is_still_in_db(functionalcaches):
    2 == functionalcaches.get('testtest', (1, 1), {})


def test_calling_add_only_occures_when_new_arguments_are_found(functionalcaches):
    @functionalcaches.cache
    def testtest(a, b):
        return a + b

    with mock.patch.object(functionalcaches, 'add',
                           wraps=functionalcaches.add) as monkey:

        # never called before here
        assert monkey.call_args is None
        assert 2 == testtest(1, 1)
        assert 2 == testtest(1, 1)
        assert 2 == testtest(1, 1)
        # still not called because it only gets the answer from db
        monkey.call_args is None

        assert 3 == testtest(1, 2)
        # finally calls add because of new arguments
        monkey.assert_called_with('testtest', (1, 2), {}, 3)
