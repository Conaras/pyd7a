# schema.py
# author: Christophe VG <contact@christophe.vg>

# base class for schema-validatable entity classes

import math

from cerberus import Validator

class ObjectValidator(Validator):
  def _validate_isinstance(self, clazz, field, value):
    if not isinstance(value, clazz):
      self._error(field, "Should be instance of " + clazz.__name__)
  
class Validatable(object):
  def __init__(self):
    self.validate()

  SCHEMA = []

  def validate(self):
    validator = ObjectValidator(
      { "item": { "oneof_schema" : self.SCHEMA, "type": "dict"} },
      allow_unknown=True
    )
    obj_dict = {}
    for attr in dir(self): obj_dict[attr] = getattr(self, attr)
    if not validator.validate({ "item" : obj_dict }):
      raise ValueError(validator.errors)

class Types(object):
  @staticmethod
  def BOOLEAN(value=None):
    b = { "type": "boolean", "nullable": False }
    if value is not None: b["allowed"] = [value]
    return b

  @staticmethod
  def BYTE():
    return { "type": "integer", "nullable": False, "min": 0, "max": 0xFF }

  @staticmethod
  def BYTES():
    return { "type": ["integer", "list"], "nullable": False, "min": 0, "max": 0xFF }

  @staticmethod
  def OBJECT(clazz=None, nullable=False):
    o = {  "nullable": nullable }
    if clazz is not None: o["isinstance"] = clazz
    return o

  @staticmethod
  def INTEGER(values=None, min=None, max=None):
    i = { "type": "integer", "nullable": False }
    if min    is not None: i["min"]     = min
    if max    is not None: i["max"]     = max
    if values is not None:
      i["allowed"] = values
      if None in values: i["nullable"] = True
    return i

  @staticmethod
  def ENUM(values):
    e = { "type": "integer", "allowed" : values}
    if None in values: e["nullable"] = True
    return e

  @staticmethod
  def BITS(length, min=0x0, max=None):
    max = max if max is not None else math.pow(2, length)-1
    return { "type": "integer", "min": 0x0, "max": max }
