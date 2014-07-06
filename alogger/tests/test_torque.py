import unittest
from alogger import log_to_dict
import os.path


class TestTorque(unittest.TestCase):

    def test_log_to_dict(self):
        directory = os.path.abspath(os.path.split(__file__)[0])
        fd = open(os.path.join(directory, 'examples/torque'))
        lines = fd.readlines()
        fd.close()

        for line in lines:
            log_to_dict(line, 'PBS')
