import time
import random
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/delay', methods=['GET'])
def serv_delay():
    delay = random.uniform(0.1, 1)
    time.sleep(delay)
    return jsonify(delay=delay)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, threaded=True)
