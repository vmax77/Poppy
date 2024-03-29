"""
    Server provides a remote control of a robot through a primitive.
    
    The client can access (get or set) all motors, sensors, primitives attached to the robot (as any primitive). The communication between the server and the client follows a predefined JSON protocol (see :mod:`~pypot.server.request` for details).
    
    So far, only one type of server has been implemented:
    
    * a zmq based server (see :mod:`~pypot.server.zmqserver`) and
    
    .. note:: All clients lives in the same primitive, so their requests are automatically combined. In future version, each client will have its own primitive.
    
    """

from zmqserver import ZMQServer