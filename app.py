from flask import Flask, jsonify, request 
import random


MAX_LOG = 1000
fish_data = {
    "cachep": [50]
}

app = Flask(__name__)

def update_data():
    global fish_data
    for fish in fish_data:
        fish_data[fish].append(fish_data[fish][-1] + random.uniform(-1,1))
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
    


