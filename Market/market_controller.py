import random


class fish_market_class:
    def __init__(self, _bias_neg: float = 0.0, _bias_pos: float = 0.0):
        self.bias_neg = - (1 + _bias_neg)
        self.bias_pos = 1 + _bias_pos
        
    def cal(self, cur):
        delta = random.uniform((2.0 / 100) * cur * self.bias_neg, (2 / 100) * cur * self.bias_pos)
        # print((2.0 / 100) * cur * self.bias_neg, (2 / 100) * cur * self.bias_pos)
        if random.randint(0,50) == 0:  
            delta = random.uniform(-10 * self.bias_neg, 10 * self.bias_pos)
        
        cur += delta
        tier = int(cur / 100)
        
        if random.randint(1, 100) <= tier:
            cur -= random.uniform(50, 100)
        
        return max(0,cur)
    
MAX_LOG = 1000

fish_data = {
    "cachep": {
        "log": [50],
        "market": fish_market_class(),
    },
    "magikarp": {
        "log": [30],
        "market": fish_market_class(0.2, 0.1),
    },
    "cakhovudai": {
        "log": [15],
        "market": fish_market_class(0.4, 0.3),
    },
    "cado": {
        "log": [25],
        "market": fish_market_class(3, 2),
    },
    "cachabac": {
        "log": [10],
        "market": fish_market_class(0.5, 0.5),
    }
}

def update_data():
    global fish_data
    for fish in fish_data:
        new_price = random.uniform(1,50)
        if "market" in fish_data[fish]:
            new_price = fish_data[fish]["market"].cal(fish_data[fish]["log"][-1])
        # print(fish,  new_price)
        fish_data[fish]["log"].append(new_price)
        if  len(fish_data[fish]) >= MAX_LOG:
            fish_data[fish].pop(0)
            
def get_fish(fish):
    return fish_data[fish]["log"][-1]

update_data()