from logging import INFO, getLogger
import unittest

from typing import Generator

from ownjoo_utils.logging.decorators import timed_generator


class TestLoggingDecorators(unittest.TestCase):
    def test_should_import(self):
        @timed_generator(log_progress=True, log_level=INFO, log_progress_interval=1, logger=getLogger(__name__))
        def log_something() -> Generator[int, None, None]:
            yield 0

        for each in log_something():
            self.assertIsNotNone(each)


if __name__ == '__main__':
    unittest.main()
