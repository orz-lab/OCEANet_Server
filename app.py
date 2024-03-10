from flask import Flask, jsonify, request 
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import random


MAX_LOG = 1000
fish_data = {
    "cachep": [50]
}

def update_data():
    print("update_data")
    global fish_data
    for fish in fish_data:
        fish_data[fish].append(fish_data[fish][-1] + random.uniform(-1,1))
        if  len(fish_data[fish]) >= MAX_LOG:
            fish_data[fish].pop(0)


app = Flask(__name__)
scheduler = BackgroundScheduler()

@app.route("/get_price")
def get_price():
    fish = request.args.get('fish') 
    if fish in fish_data:
        return jsonify({'price': fish_data[fish][-1]}) 
    return jsonify({}) 


scheduler.add_job(func=update_data, trigger="interval", seconds=0.2)


if __name__ == '__main__':
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    app.run()
    


