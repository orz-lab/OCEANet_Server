from flask import Flask, jsonify, request 
from flask_apscheduler import APScheduler
import atexit
import random


MAX_LOG = 1000
fish_data = {
    "cachep": [50]
}

class Config:
    SCHEDULER_API_ENABLED = True
    
app = Flask(__name__)
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@scheduler.task('interval', id='do_job_1', seconds=0.2)
def update_data():
    print("update_data")
    global fish_data
    for fish in fish_data:
        fish_data[fish].append(fish_data[fish][-1] + random.uniform(-1,1))
        if  len(fish_data[fish]) >= MAX_LOG:
            fish_data[fish].pop(0)

@app.route("/get_price")
def get_price():
    fish = request.args.get('fish') 
    if fish in fish_data:
        return jsonify({'price': fish_data[fish][-1]}) 
    return jsonify({}) 

if __name__ == '__main__':
    app.run()
    


