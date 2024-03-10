from flask import Flask, jsonify, request 
from threading import Timer
import random


MAX_LOG = 1000
fish_data = {
    "cachep": [50]
}

def update_data(interval):
    print("update_data")
    Timer(interval, update_data, [interval]).start()
    global fish_data
    for fish in fish_data:
        fish_data[fish].append(fish_data[fish][-1] + random.uniform(-1,1))
        if  len(fish_data[fish]) >= MAX_LOG:
            fish_data[fish].pop(0)


app = Flask(__name__)

@app.route("/get_price")
def get_price():
    fish = request.args.get('fish') 
    if fish in fish_data:
        return jsonify({'price': fish_data[fish][-1]}) 
    return jsonify({}) 

if __name__ == '__main__':
    update_data(1)
    app.run()



