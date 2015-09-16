# parser
# author: Christophe VG <contact@christophe.vg>

# a parser for ALP commands

from bitstring                    import ConstBitStream, ReadError

from d7a.types.ct                 import CT
from d7a.sp.status                import Status
from d7a.tp.addressee             import Addressee
from d7a.alp.command              import Command
from d7a.alp.payload              import Payload
from d7a.alp.action               import Action
from d7a.alp.operations.responses import ReturnFileData
from d7a.alp.operands.file        import Offset, Data

class Parser(object):

  def __init__(self):
    self.buffer = []

  def reset(self):
    self.buffer = []
    return self

  def shift_buffer(self, start):
    self.buffer = self.buffer[start:]
    return self

  def parse(self, msg):
    self.buffer.extend(msg)
    return self.parse_buffer()
    
  def parse_buffer(self):
    parsed = 0
    cmds   = []

    while True:
      (cmd, info) = self.parse_one_command_from_buffer()
      if cmd is None: break
      parsed += info["parsed"]
      cmds.append(cmd)
      
    info["parsed"] = parsed
    return (cmds, info)

  def parse_one_command_from_buffer(self):
    self.s = ConstBitStream(bytes=self.buffer)
    try:
      cmd = self.parse_alp_command()
      bits_parsed = self.s.pos
      self.shift_buffer(bits_parsed/8)
    except ReadError:
      cmd = None
      bits_parsed = 0
      
    info = {
      "parsed" : bits_parsed,
      "buffer" : len(self.buffer) * 8
    }
    return (cmd, info)    

  def parse_alp_command(self):
    interface = None
    group     = None
    resp      = None
    opcode    = None
    operation = None
    error     = None
    _         = self.parse_alp_interface_id()
    return Command(
      interface = self.parse_alp_interface_status(),
      payload   = self.parse_alp_payload()
    )

  def parse_alp_interface_id(self):
    b = self.s.read("uint:8")
    if b != 0xd7: raise Exception("expected 0xd7, found {0}".format(b))

  def parse_alp_interface_status(self):
    nls         = self.s.read("bool")
    missed      = self.s.read("bool")
    retry       = self.s.read("bool")
    _           = self.s.read("pad:2" )
    state       = self.s.read("uint:3")
    fifo_token  = self.s.read("uint:8")
    request_id  = self.s.read("uint:8")
    response_to = self.parse_ct()
    addressee   = self.parse_addressee()

    return Status(nls=nls, missed=missed, retry=retry, state=state,
                  fifo_token=fifo_token, request_id=request_id,
                  response_to=response_to, addressee=addressee)

  def parse_ct(self):
    exp  = self.s.read("uint:3")
    mant = self.s.read("uint:5")
    return CT(exp=exp, mant=mant)

  def parse_addressee(self):
    _     = self.s.read("pad:2")
    hasid = self.s.read("bool")
    vid   = self.s.read("bool")
    cl    = self.s.read("uint:4")
    l     = Addressee.length_for(hasid=hasid,vid=vid)
    id    = self.s.read("uint:"+str(l*8)) if l > 0 else None
    return Addressee(hasid=hasid, vid=vid, cl=cl, id=id)

  def parse_alp_payload(self):
    # TODO: extend to multiple actions, only one supported right now
    action = self.parse_alp_action()
    return Payload(actions=[action])

  def parse_alp_action(self):
    group     = self.s.read("bool")
    resp      = self.s.read("bool")
    op        = self.s.read("uint:6")
    try:
      operation = {
        32 : self.parse_alp_return_file_data_operation
      }[op]()
    except KeyError:
      raise NotImplementedError("alp_action " + str(op) + " is not implemented")
    return Action(group=group, resp=resp, operation=operation)

  def parse_alp_return_file_data_operation(self):
    operand = self.parse_alp_return_file_data_operand()
    return ReturnFileData(operand=operand)

  def parse_alp_return_file_data_operand(self):
    offset = self.parse_offset()
    length = self.s.read("uint:8")
    data   = self.s.read("bytes:" + str(length))
    return Data(offset=offset, data=map(ord,data))

  def parse_offset(self):
    id     = self.s.read("uint:8")
    size   = self.s.read("uint:2") # + 1 = already read
    
    offset = self.s.read("uint:" + str(6+(size * 8)))
    return Offset(id=id, size=size+1, offset=offset)
