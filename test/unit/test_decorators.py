from logging import INFO
import unittest

from typing import Generator


class TestLoggingDecorators(unittest.TestCase):
    def test_should_import(self):
        try:
            from utils import timed_generator
            @timed_generator(log_progress=True, log_level=INFO, log_progress_interval=1)
            def log_something() -> Generator[int, None, None]:
                yield 0

            for each in log_something():
                self.assertIsNotNone(each)

        except Exception as e:
            self.assertTrue(False, msg=e)


if __name__ == '__main__':
    unittest.main()
