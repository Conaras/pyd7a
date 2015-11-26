from d7a.support.schema import Validatable, Types

class Control(Validatable):

  SCHEMA = [{
    "has_network_layer_security": Types.BOOLEAN(),
    "has_multi_hop": Types.BOOLEAN(),
    "has_origin_access_id": Types.BOOLEAN(),
    "is_origin_access_id_vid": Types.BOOLEAN(),
    "origin_access_class": Types.INTEGER(min=0, max=15)
  }]

  def __init__(self, has_network_layer_security, has_multi_hop,
               has_origin_access_id, is_origin_access_id_vid, origin_access_class):
    self.has_network_layer_security = has_network_layer_security
    self.has_multi_hop = has_multi_hop
    self.has_origin_access_id = has_origin_access_id
    self.is_origin_access_id_vid = is_origin_access_id_vid
    self.origin_access_class = origin_access_class
    super(Control, self).__init__()