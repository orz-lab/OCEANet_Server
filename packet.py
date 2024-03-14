import json
import enum


class Action(enum.Enum):
    Update_price = enum.auto()
    ConnectOk = enum.auto()
    ConnectDeny = enum.auto()
    Connect = enum.auto()
    Update_inventory = enum.auto()
    Get_inventory = enum.auto()
    Send_inventory = enum.auto()
    

class Packet:
    def __init__(self, action: Action, *payloads):
        self.action: Action = action
        self.payloads: tuple = payloads

    def __str__(self) -> str:
        serialize_dict = {'a': self.action.name}
        for i in range(len(self.payloads)):
            serialize_dict[f'p{i}'] = self.payloads[i]
        data = json.dumps(serialize_dict, separators=(',', ':'))
        return data

    def __bytes__(self) -> bytes:
        return str(self).encode('utf-8')

class Update_pricePacket(Packet):
    def __init__(self, *message):
        super().__init__(Action.Update_price, message)
    
class Update_inventoryPacket(Packet):
    def __init__(self, username: str, password: str, money: float, fish_inventory: list):
        super().__init__(Action.Update_inventory, username, password, money, fish_inventory)  

class Get_inventoryPacket(Packet):
    def __init__(self, username: str):
        super().__init__(Action.Get_inventory, username)  

class Send_inventoryPacket(Packet):
    def __init__(self, money: float, fish_inventory: list):
        super().__init__(Action.Send_inventory, money, fish_inventory)  

class ConnectOkPacket(Packet):
    def __init__(self):
        super().__init__(Action.ConnectOk)

class ConnectDenyPacket(Packet):
    def __init__(self, reason: str):
        super().__init__(Action.ConnectDeny, reason)

class ConnectPacket(Packet):
    def __init__(self, username: str, password: str):
        super().__init__(Action.Connect, username, password)

def from_json(json_str: str) -> Packet:
    obj_dict = json.loads(json_str)

    action = None
    payloads = []
    for key, value in obj_dict.items():
        if key == 'a':
            action = value

        elif key[0] == 'p':
            index = int(key[1:])
            payloads.insert(index, value)

    class_name = action + "Packet"
    try:
        constructor: type = globals()[class_name]
        return constructor(*payloads)
    except KeyError as e:
        print(
            f"{class_name} is not a valid packet name. Stacktrace: {e}")
    except TypeError:
        print(
            f"{class_name} can't handle arguments {tuple(payloads)}.")