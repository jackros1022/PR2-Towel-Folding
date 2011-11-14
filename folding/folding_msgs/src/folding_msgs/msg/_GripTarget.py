"""autogenerated by genmsg_py from GripTarget.msg. Do not edit."""
import roslib.message
import struct

import geometry_msgs.msg
import std_msgs.msg

class GripTarget(roslib.message.Message):
  _md5sum = "d498fe7192b5922bafbc9809932e496c"
  _type = "folding_msgs/GripTarget"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """geometry_msgs/PointStamped point
string arm
bool grip
float64 pitch
float64 roll
float64 yaw
bool empty

================================================================================
MSG: geometry_msgs/PointStamped
# This represents a Point with reference coordinate frame and timestamp
Header header
Point point

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.secs: seconds (stamp_secs) since epoch
# * stamp.nsecs: nanoseconds since stamp_secs
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

"""
  __slots__ = ['point','arm','grip','pitch','roll','yaw','empty']
  _slot_types = ['geometry_msgs/PointStamped','string','bool','float64','float64','float64','bool']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.
    
    The available fields are:
       point,arm,grip,pitch,roll,yaw,empty
    
    @param args: complete set of field values, in .msg order
    @param kwds: use keyword arguments corresponding to message field names
    to set specific fields. 
    """
    if args or kwds:
      super(GripTarget, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.point is None:
        self.point = geometry_msgs.msg.PointStamped()
      if self.arm is None:
        self.arm = ''
      if self.grip is None:
        self.grip = False
      if self.pitch is None:
        self.pitch = 0.
      if self.roll is None:
        self.roll = 0.
      if self.yaw is None:
        self.yaw = 0.
      if self.empty is None:
        self.empty = False
    else:
      self.point = geometry_msgs.msg.PointStamped()
      self.arm = ''
      self.grip = False
      self.pitch = 0.
      self.roll = 0.
      self.yaw = 0.
      self.empty = False

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    @param buff: buffer
    @type  buff: StringIO
    """
    try:
      _x = self
      buff.write(_struct_3I.pack(_x.point.header.seq, _x.point.header.stamp.secs, _x.point.header.stamp.nsecs))
      _x = self.point.header.frame_id
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_struct_3d.pack(_x.point.point.x, _x.point.point.y, _x.point.point.z))
      _x = self.arm
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_struct_B3dB.pack(_x.grip, _x.pitch, _x.roll, _x.yaw, _x.empty))
    except struct.error, se: self._check_types(se)
    except TypeError, te: self._check_types(te)

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    @param str: byte array of serialized message
    @type  str: str
    """
    try:
      if self.point is None:
        self.point = geometry_msgs.msg.PointStamped()
      end = 0
      _x = self
      start = end
      end += 12
      (_x.point.header.seq, _x.point.header.stamp.secs, _x.point.header.stamp.nsecs,) = _struct_3I.unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.point.header.frame_id = str[start:end]
      _x = self
      start = end
      end += 24
      (_x.point.point.x, _x.point.point.y, _x.point.point.z,) = _struct_3d.unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.arm = str[start:end]
      _x = self
      start = end
      end += 26
      (_x.grip, _x.pitch, _x.roll, _x.yaw, _x.empty,) = _struct_B3dB.unpack(str[start:end])
      self.grip = bool(self.grip)
      self.empty = bool(self.empty)
      return self
    except struct.error, e:
      raise roslib.message.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    @param buff: buffer
    @type  buff: StringIO
    @param numpy: numpy python module
    @type  numpy module
    """
    try:
      _x = self
      buff.write(_struct_3I.pack(_x.point.header.seq, _x.point.header.stamp.secs, _x.point.header.stamp.nsecs))
      _x = self.point.header.frame_id
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_struct_3d.pack(_x.point.point.x, _x.point.point.y, _x.point.point.z))
      _x = self.arm
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_struct_B3dB.pack(_x.grip, _x.pitch, _x.roll, _x.yaw, _x.empty))
    except struct.error, se: self._check_types(se)
    except TypeError, te: self._check_types(te)

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    @param str: byte array of serialized message
    @type  str: str
    @param numpy: numpy python module
    @type  numpy: module
    """
    try:
      if self.point is None:
        self.point = geometry_msgs.msg.PointStamped()
      end = 0
      _x = self
      start = end
      end += 12
      (_x.point.header.seq, _x.point.header.stamp.secs, _x.point.header.stamp.nsecs,) = _struct_3I.unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.point.header.frame_id = str[start:end]
      _x = self
      start = end
      end += 24
      (_x.point.point.x, _x.point.point.y, _x.point.point.z,) = _struct_3d.unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.arm = str[start:end]
      _x = self
      start = end
      end += 26
      (_x.grip, _x.pitch, _x.roll, _x.yaw, _x.empty,) = _struct_B3dB.unpack(str[start:end])
      self.grip = bool(self.grip)
      self.empty = bool(self.empty)
      return self
    except struct.error, e:
      raise roslib.message.DeserializationError(e) #most likely buffer underfill

_struct_I = roslib.message.struct_I
_struct_3I = struct.Struct("<3I")
_struct_B3dB = struct.Struct("<B3dB")
_struct_3d = struct.Struct("<3d")