
from d7a.support.schema import Validatable, Types
from d7a.d7atp.control import Control
from d7a.types.ct import CT
from d7a.alp.command import Command

class Frame(Validatable):

  SCHEMA = [{
    "control": Types.OBJECT(Control),
    "dialog_id": Types.INTEGER(min=0, max=255),
    "transaction_id": Types.INTEGER(min=0, max=255),
    "timeout_template": Types.OBJECT(CT, nullable=True),
    "ack_template": Types.OBJECT(nullable=True),
    "alp_command": Types.OBJECT(Command)
  }]

  def __init__(self, control, dialog_id, transaction_id, timeout_template, ack_template, alp_command):
    self.control = control
    self.dialog_id = dialog_id
    self.transaction_id = transaction_id
    self.timeout_template = timeout_template
    self.ack_template = ack_template
    self.alp_command = alp_command
    super(Frame, self).__init__()