from flask import Flask, jsonify, request 
import random


MAX_LOG = 1000
fish_data = {
    "cachep": [50]
}

app = Flask(__name__)

class cachep_delta_class:
    count = 0
    
    def cal(self, delta):
        delta = random.uniform(-2, 2)
        if random.randint(0,50) == 0:  
            delta = random.uniform(-10,10)
        
        if random.uniform(0,1) <= 0.25 ** self.count:
            if delta > 0:
                delta = -abs(delta)
            else:
                delta = abs(delta)
        
        if delta > 0:
            self.count += 1
        else:
            self.count -= 1
        
        return delta

cachep_delta = cachep_delta_class()

def update_data():
    global fish_data
    for fish in fish_data:
        delta = random.uniform(-1,1)
        
        if fish == "cachep":
            delta = cachep_delta.cal(delta)
                
        fish_data[fish].append(fish_data[fish][-1] + delta)
        if  len(fish_data[fish]) >= MAX_LOG:
            fish_data[fish].pop(0)

@app.route("/get_price")
def get_price():
    update_data()
    fish = request.args.get('fish') 
    if fish in fish_data:
        return jsonify({'price': fish_data[fish][-1]}) 
    return jsonify({}) 

if __name__ == '__main__':
    app.run(port=80)
    


