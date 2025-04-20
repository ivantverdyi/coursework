import time
import random
from flask import Flask, Response
import json

app = Flask(__name__)

@app.route('/delay', methods=['GET'])
def serv_delay():
    delay = random.uniform(0.1, 1)
    time.sleep(delay)
    return Response(json.dumps({'delay': delay}), content_type='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
