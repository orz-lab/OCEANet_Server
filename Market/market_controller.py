import random


class fish_market_class:
    def __init__(self, _bias_neg: float = 0.0, _bias_pos: float = 0.0):
        self.bias_neg = 1 - _bias_neg
        self.bias_pos = 1 + _bias_pos
        
    def cal(self, delta):
        delta = random.uniform(-2 * self.bias_neg, 2 * self.bias_pos)
        if random.randint(0,50) == 0:  
            delta = random.uniform(-10 * self.bias_neg, 10 * self.bias_pos)
        
        return delta
    
MAX_LOG = 1000

fish_data = {
    "cachep": {
        "log": [50],
        "market": fish_market_class(),
    },
    "magikarp": {
        "log": [30],
        "market": fish_market_class(0.1, 0.1),
    },
    "cakhovudai": {
        "log": [15],
        "market": fish_market_class(0.3, 0.3),
    },
    "cado": {
        "log": [25],
        "market": fish_market_class(2, 2),
    },
    "cachabac": {
        "log": [10],
        "market": fish_market_class(0.5, 0.5),
    }
}

def update_data():
    global fish_data
    for fish in fish_data:
        delta = random.uniform(-1,1)
        
        if "market" in fish_data[fish]:
            delta = fish_data[fish]["market"].cal(delta)
                
        fish_data[fish]["log"].append(fish_data[fish]["log"][-1] + delta)
        if  len(fish_data[fish]) >= MAX_LOG:
            fish_data[fish].pop(0)
            
def get_fish(fish):
    return fish_data[fish]["log"][-1]
