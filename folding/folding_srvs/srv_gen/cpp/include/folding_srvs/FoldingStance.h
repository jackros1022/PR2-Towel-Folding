/* Auto-generated by genmsg_cpp for file /home/karthik/karthik_sandbox/github_repos/folding/folding_srvs/srv/FoldingStance.srv */
#ifndef FOLDING_SRVS_SERVICE_FOLDINGSTANCE_H
#define FOLDING_SRVS_SERVICE_FOLDINGSTANCE_H
#include <string>
#include <vector>
#include <ostream>
#include "ros/serialization.h"
#include "ros/builtin_message_traits.h"
#include "ros/message_operations.h"
#include "ros/message.h"
#include "ros/time.h"

#include "ros/service_traits.h"




namespace folding_srvs
{
template <class ContainerAllocator>
struct FoldingStanceRequest_ : public ros::Message
{
  typedef FoldingStanceRequest_<ContainerAllocator> Type;

  FoldingStanceRequest_()
  {
  }

  FoldingStanceRequest_(const ContainerAllocator& _alloc)
  {
  }


private:
  static const char* __s_getDataType_() { return "folding_srvs/FoldingStanceRequest"; }
public:
  ROS_DEPRECATED static const std::string __s_getDataType() { return __s_getDataType_(); }

  ROS_DEPRECATED const std::string __getDataType() const { return __s_getDataType_(); }

private:
  static const char* __s_getMD5Sum_() { return "d41d8cd98f00b204e9800998ecf8427e"; }
public:
  ROS_DEPRECATED static const std::string __s_getMD5Sum() { return __s_getMD5Sum_(); }

  ROS_DEPRECATED const std::string __getMD5Sum() const { return __s_getMD5Sum_(); }

private:
  static const char* __s_getServerMD5Sum_() { return "d41d8cd98f00b204e9800998ecf8427e"; }
public:
  ROS_DEPRECATED static const std::string __s_getServerMD5Sum() { return __s_getServerMD5Sum_(); }

  ROS_DEPRECATED const std::string __getServerMD5Sum() const { return __s_getServerMD5Sum_(); }

private:
  static const char* __s_getMessageDefinition_() { return "\n\
"; }
public:
  ROS_DEPRECATED static const std::string __s_getMessageDefinition() { return __s_getMessageDefinition_(); }

  ROS_DEPRECATED const std::string __getMessageDefinition() const { return __s_getMessageDefinition_(); }

  ROS_DEPRECATED virtual uint8_t *serialize(uint8_t *write_ptr, uint32_t seq) const
  {
    ros::serialization::OStream stream(write_ptr, 1000000000);
    return stream.getData();
  }

  ROS_DEPRECATED virtual uint8_t *deserialize(uint8_t *read_ptr)
  {
    ros::serialization::IStream stream(read_ptr, 1000000000);
    return stream.getData();
  }

  ROS_DEPRECATED virtual uint32_t serializationLength() const
  {
    uint32_t size = 0;
    return size;
  }

  typedef boost::shared_ptr< ::folding_srvs::FoldingStanceRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::folding_srvs::FoldingStanceRequest_<ContainerAllocator>  const> ConstPtr;
}; // struct FoldingStanceRequest
typedef  ::folding_srvs::FoldingStanceRequest_<std::allocator<void> > FoldingStanceRequest;

typedef boost::shared_ptr< ::folding_srvs::FoldingStanceRequest> FoldingStanceRequestPtr;
typedef boost::shared_ptr< ::folding_srvs::FoldingStanceRequest const> FoldingStanceRequestConstPtr;


template <class ContainerAllocator>
struct FoldingStanceResponse_ : public ros::Message
{
  typedef FoldingStanceResponse_<ContainerAllocator> Type;

  FoldingStanceResponse_()
  {
  }

  FoldingStanceResponse_(const ContainerAllocator& _alloc)
  {
  }


private:
  static const char* __s_getDataType_() { return "folding_srvs/FoldingStanceResponse"; }
public:
  ROS_DEPRECATED static const std::string __s_getDataType() { return __s_getDataType_(); }

  ROS_DEPRECATED const std::string __getDataType() const { return __s_getDataType_(); }

private:
  static const char* __s_getMD5Sum_() { return "d41d8cd98f00b204e9800998ecf8427e"; }
public:
  ROS_DEPRECATED static const std::string __s_getMD5Sum() { return __s_getMD5Sum_(); }

  ROS_DEPRECATED const std::string __getMD5Sum() const { return __s_getMD5Sum_(); }

private:
  static const char* __s_getServerMD5Sum_() { return "d41d8cd98f00b204e9800998ecf8427e"; }
public:
  ROS_DEPRECATED static const std::string __s_getServerMD5Sum() { return __s_getServerMD5Sum_(); }

  ROS_DEPRECATED const std::string __getServerMD5Sum() const { return __s_getServerMD5Sum_(); }

private:
  static const char* __s_getMessageDefinition_() { return "\n\
\n\
"; }
public:
  ROS_DEPRECATED static const std::string __s_getMessageDefinition() { return __s_getMessageDefinition_(); }

  ROS_DEPRECATED const std::string __getMessageDefinition() const { return __s_getMessageDefinition_(); }

  ROS_DEPRECATED virtual uint8_t *serialize(uint8_t *write_ptr, uint32_t seq) const
  {
    ros::serialization::OStream stream(write_ptr, 1000000000);
    return stream.getData();
  }

  ROS_DEPRECATED virtual uint8_t *deserialize(uint8_t *read_ptr)
  {
    ros::serialization::IStream stream(read_ptr, 1000000000);
    return stream.getData();
  }

  ROS_DEPRECATED virtual uint32_t serializationLength() const
  {
    uint32_t size = 0;
    return size;
  }

  typedef boost::shared_ptr< ::folding_srvs::FoldingStanceResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::folding_srvs::FoldingStanceResponse_<ContainerAllocator>  const> ConstPtr;
}; // struct FoldingStanceResponse
typedef  ::folding_srvs::FoldingStanceResponse_<std::allocator<void> > FoldingStanceResponse;

typedef boost::shared_ptr< ::folding_srvs::FoldingStanceResponse> FoldingStanceResponsePtr;
typedef boost::shared_ptr< ::folding_srvs::FoldingStanceResponse const> FoldingStanceResponseConstPtr;

struct FoldingStance
{

typedef FoldingStanceRequest Request;
typedef FoldingStanceResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;
}; // struct FoldingStance
} // namespace folding_srvs

namespace ros
{
namespace message_traits
{
template<class ContainerAllocator>
struct MD5Sum< ::folding_srvs::FoldingStanceRequest_<ContainerAllocator> > {
  static const char* value() 
  {
    return "d41d8cd98f00b204e9800998ecf8427e";
  }

  static const char* value(const  ::folding_srvs::FoldingStanceRequest_<ContainerAllocator> &) { return value(); } 
  static const uint64_t static_value1 = 0xd41d8cd98f00b204ULL;
  static const uint64_t static_value2 = 0xe9800998ecf8427eULL;
};

template<class ContainerAllocator>
struct DataType< ::folding_srvs::FoldingStanceRequest_<ContainerAllocator> > {
  static const char* value() 
  {
    return "folding_srvs/FoldingStanceRequest";
  }

  static const char* value(const  ::folding_srvs::FoldingStanceRequest_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator>
struct Definition< ::folding_srvs::FoldingStanceRequest_<ContainerAllocator> > {
  static const char* value() 
  {
    return "\n\
";
  }

  static const char* value(const  ::folding_srvs::FoldingStanceRequest_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator> struct IsFixedSize< ::folding_srvs::FoldingStanceRequest_<ContainerAllocator> > : public TrueType {};
} // namespace message_traits
} // namespace ros


namespace ros
{
namespace message_traits
{
template<class ContainerAllocator>
struct MD5Sum< ::folding_srvs::FoldingStanceResponse_<ContainerAllocator> > {
  static const char* value() 
  {
    return "d41d8cd98f00b204e9800998ecf8427e";
  }

  static const char* value(const  ::folding_srvs::FoldingStanceResponse_<ContainerAllocator> &) { return value(); } 
  static const uint64_t static_value1 = 0xd41d8cd98f00b204ULL;
  static const uint64_t static_value2 = 0xe9800998ecf8427eULL;
};

template<class ContainerAllocator>
struct DataType< ::folding_srvs::FoldingStanceResponse_<ContainerAllocator> > {
  static const char* value() 
  {
    return "folding_srvs/FoldingStanceResponse";
  }

  static const char* value(const  ::folding_srvs::FoldingStanceResponse_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator>
struct Definition< ::folding_srvs::FoldingStanceResponse_<ContainerAllocator> > {
  static const char* value() 
  {
    return "\n\
\n\
";
  }

  static const char* value(const  ::folding_srvs::FoldingStanceResponse_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator> struct IsFixedSize< ::folding_srvs::FoldingStanceResponse_<ContainerAllocator> > : public TrueType {};
} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

template<class ContainerAllocator> struct Serializer< ::folding_srvs::FoldingStanceRequest_<ContainerAllocator> >
{
  template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
  {
  }

  ROS_DECLARE_ALLINONE_SERIALIZER;
}; // struct FoldingStanceRequest_
} // namespace serialization
} // namespace ros


namespace ros
{
namespace serialization
{

template<class ContainerAllocator> struct Serializer< ::folding_srvs::FoldingStanceResponse_<ContainerAllocator> >
{
  template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
  {
  }

  ROS_DECLARE_ALLINONE_SERIALIZER;
}; // struct FoldingStanceResponse_
} // namespace serialization
} // namespace ros

namespace ros
{
namespace service_traits
{
template<>
struct MD5Sum<folding_srvs::FoldingStance> {
  static const char* value() 
  {
    return "d41d8cd98f00b204e9800998ecf8427e";
  }

  static const char* value(const folding_srvs::FoldingStance&) { return value(); } 
};

template<>
struct DataType<folding_srvs::FoldingStance> {
  static const char* value() 
  {
    return "folding_srvs/FoldingStance";
  }

  static const char* value(const folding_srvs::FoldingStance&) { return value(); } 
};

template<class ContainerAllocator>
struct MD5Sum<folding_srvs::FoldingStanceRequest_<ContainerAllocator> > {
  static const char* value() 
  {
    return "d41d8cd98f00b204e9800998ecf8427e";
  }

  static const char* value(const folding_srvs::FoldingStanceRequest_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator>
struct DataType<folding_srvs::FoldingStanceRequest_<ContainerAllocator> > {
  static const char* value() 
  {
    return "folding_srvs/FoldingStance";
  }

  static const char* value(const folding_srvs::FoldingStanceRequest_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator>
struct MD5Sum<folding_srvs::FoldingStanceResponse_<ContainerAllocator> > {
  static const char* value() 
  {
    return "d41d8cd98f00b204e9800998ecf8427e";
  }

  static const char* value(const folding_srvs::FoldingStanceResponse_<ContainerAllocator> &) { return value(); } 
};

template<class ContainerAllocator>
struct DataType<folding_srvs::FoldingStanceResponse_<ContainerAllocator> > {
  static const char* value() 
  {
    return "folding_srvs/FoldingStance";
  }

  static const char* value(const folding_srvs::FoldingStanceResponse_<ContainerAllocator> &) { return value(); } 
};

} // namespace service_traits
} // namespace ros

#endif // FOLDING_SRVS_SERVICE_FOLDINGSTANCE_H
