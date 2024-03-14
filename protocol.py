import queue
import packet
from autobahn.twisted.websocket import WebSocketServerProtocol
import Market.market_controller as Market
import Market.users as usersData

class GameServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self._packet_queue: queue.Queue[tuple['GameServerProtocol', packet.Packet]] = queue.Queue()
        self._state: callable = None
        self._state = self.PLAY

    def PLAY(self, sender: 'GameServerProtocol', p: packet.Packet):
        # print(p.action)
        
        match p.action:
            case packet.Action.Update_price:
                Market.update_data()
                # if sender == self:
                #     self.broadcast(p, exclude_self=True)
                # else:
                fishes = []
        
                for id in range(len(p.payloads[0])):
                    fish = p.payloads[0][id]
                    if fish in Market.fish_data:
                        fishes.append({fish: Market.get_fish(fish)})
                p = packet.Packet(p.action, fishes)
                self.send_client(p)
            
            case packet.Action.Update_inventory:
                username, password, money, fish_inventory = p.payloads
                # print(p.payloads)
                usersData.update_inventory(username, password, money, fish_inventory)
            
            case packet.Action.Get_inventory:
                username = p.payloads[0]

                money, fish_inventory = usersData.get_inventory(username)
                
                if fish_inventory == {}:
                    return
                # print(money, fish_inventory)
                
                p = packet.Send_inventoryPacket(money, fish_inventory)
                
                self.send_client(p)
    
            case packet.Action.Connect:
                username, password = p.payloads
                
                # print(username, password)
                
                if usersData.is_has_user(username):
                    if usersData.login_check(username, password):
                        # print(username, password)
                        self.send_client(packet.ConnectOkPacket())
                        return
                    self.send_client(packet.ConnectDenyPacket("Username or password incorrect"))
                    return
                
                if usersData.make_new_user(username, password):
                    self.send_client(packet.ConnectOkPacket())
                    return
                
                self.send_client(packet.ConnectDenyPacket("Username or password incorrect"))
            

    def tick(self):
        # Process the next packet in the queue
        if not self._packet_queue.empty():
            s, p = self._packet_queue.get()
            self._state(s, p)

    def broadcast(self, p: packet.Packet, exclude_self: bool = False):
        for other in self.factory.players:
            if other == self and exclude_self:
                continue
            other.onPacket(self, p)

    # Override
    def onConnect(self, request):
        print(f"Client connecting: {request.peer}")

    # Override
    def onOpen(self):
        print(f"Websocket connection open.")

    # Override
    def onClose(self, wasClean, code, reason):
        self.factory.players.remove(self)
        print(f"Websocket connection closed{' unexpectedly' if not wasClean else ' cleanly'} with code {code}: {reason}")

    # Override
    def onMessage(self, payload, isBinary):
        decoded_payload = payload.decode('utf-8')

        try:
            p: packet.Packet = packet.from_json(decoded_payload)
        except Exception as e:
            print(f"Could not load message as packet: {e}. Message was: {payload.decode('utf8')}")

        self.onPacket(self, p)

    def onPacket(self, sender: 'GameServerProtocol', p: packet.Packet):
        self._packet_queue.put((sender, p))
        # print(f"Queued packet: {p}")

    def send_client(self, p: packet.Packet):
        b = bytes(p)
        self.sendMessage(b)