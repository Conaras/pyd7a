# configuration.py
# author: Christophe VG <contact@christophe.vg>

# unit tests for the D7A SP (FIFO) Configuration

import unittest
from d7a.sp.session import States

from d7a.types.ct         import CT
from d7a.sp.qos           import QoS
from d7a.sp.configuration import Configuration

class TestConfiguration(unittest.TestCase):
  def test_default_constructor(self):
    c = Configuration()

  def test_invalid_configuration_construction(self):
    def bad(args, kwargs): Configuration(**kwargs)
    self.assertRaises(ValueError, bad, [], { "qos"       : None  })
    self.assertRaises(ValueError, bad, [], { "addressee" : None  })
    self.assertRaises(ValueError, bad, [], { "dorm_to"   : None  })

  def test_configuration_bad_composed_objects(self):
    def bad(args, kwargs): Configuration(**kwargs)
    self.assertRaises(ValueError, bad, [], { "qos":       CT()  })
    self.assertRaises(ValueError, bad, [], { "dorm_to":   QoS() })
    self.assertRaises(ValueError, bad, [], { "addressee": QoS() })

  def test_byte_generation(self):
    # TODO: use mocking framework to mock sub-objects
    bytes = bytearray(Configuration())
    self.assertEqual(len(bytes), 4)
    self.assertEquals(bytes[0], int( '00000000', 2)) # qos
    self.assertEquals(bytes[1], int( '00000000', 2)) # dorm_to (CT)
    self.assertEquals(bytes[2], int( '00010000', 2)) # addressee control NOID
    self.assertEquals(bytes[3], 0)  # access class


if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestConfiguration)
  unittest.TextTestRunner(verbosity=1).run(suite)
