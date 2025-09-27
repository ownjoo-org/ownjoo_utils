import unittest
from datetime import datetime
from typing import Optional

from ownjoo_utils.parsing.consts import TimeFormats
from ownjoo_utils.parsing.types import exp_type, str_to_list, get_datetime


class TestParsingFunctions(unittest.TestCase):
    def test_should_get_expected_type(self):
        # setup
        expected: str = 'blah'

        # execute
        actual = exp_type(v=expected, exp=str, default='')

        # assess
        self.assertEqual(expected, actual)

        # teardown

    def test_should_get_default_type(self):
        # setup
        expected: str = ''

        # execute
        actual = exp_type(v=[], exp=str, default=expected)

        # assess
        self.assertEqual(expected, actual)

        # teardown

    def test_should_get_list_from_str(self):
        # setup
        expected: list = ['a', 'b', 'c']
        sep: str = ';'

        # execute
        actual = str_to_list(v=sep.join(expected), separator=sep)

        # assess
        self.assertEqual(expected, actual)

        # teardown

    def test_should_get_exp_list_from_str(self):
        # setup
        expected: list = ['a', 'b', 'c']

        # execute
        actual = exp_type(v=','.join(expected), exp=list)

        # assess
        self.assertEqual(expected, actual)

        # teardown

    def test_should_get_exp_dict(self):
        # setup
        expected: dict = {0: 'a', 1: 'b', 2: 'c'}

        # execute
        actual = exp_type(v=expected, exp=dict)

        # assess
        self.assertEqual(expected, actual)

        # teardown

    def test_should_get_default_dict(self):
        # setup
        expected: dict = {}

        # execute
        actual = exp_type(v='not a dict', exp=dict, default={})

        # assess
        self.assertEqual(expected, actual)

        # teardown

    def test_should_get_none(self):
        # setup
        expected: Optional[dict] = None

        # execute
        actual = exp_type(v='not a dict', exp=dict)

        # assess
        self.assertEqual(expected, actual)

        # teardown

    def test_should_get_valid(self):
        # setup
        expected: str = 'blah'

        # execute
        actual = exp_type(v=expected, exp=str, validator=lambda x, *args, **kwargs: x == expected)

        # assess
        self.assertEqual(expected, actual)

        # teardown

    def test_should_get_default_on_validation_fail(self):
        # setup
        expected: str = ''

        # execute
        actual = exp_type(v='blah', exp=str, validator=lambda x, *args, **kwargs: x is None, default=expected)

        # assess
        self.assertEqual(expected, actual)

        # teardown

    def test_should_convert(self):
        # setup
        expected: str = 'blah'
        unwanted: str = '_more'

        # execute
        actual = exp_type(
            v=f'{expected}{unwanted}',
            exp=str,
            converter=lambda x, *args, **kwargs: x.removesuffix(unwanted),
            validator=lambda x, *args, **kwargs: x == expected,
        )

        # assess
        self.assertEqual(expected, actual)

        # teardown

    def test_should_get_time_formats(self):
        # setup

        # execute/assess
        for format_str in TimeFormats:
            self.assertIsNotNone(format_str)
            self.assertIsNotNone(format_str.value)

        # teardown

    def test_should_get_datetime_from_str(self):
        # setup
        expected: str = 'Sun, 06 Nov 1994 08:49:37 GMT'

        # execute
        actual: datetime = get_datetime(v=expected, exp=datetime)

        # assess
        self.assertIsInstance(actual, datetime)

        # teardown

    def test_should_get_datetime_from_float(self):
        # setup
        expected: float = datetime.now().timestamp()

        # execute
        actual: datetime = get_datetime(v=expected, exp=datetime)

        # assess
        self.assertIsInstance(expected, float)
        self.assertIsInstance(actual, datetime)

        # teardown


if __name__ == '__main__':
    unittest.main()
