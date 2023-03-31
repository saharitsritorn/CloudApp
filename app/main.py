import pymysql
from flask import jsonify
import json
import sys
import os
from flask import Flask
import subprocess
import threading
app = Flask(__name__)

@app.route('/', methods=['GET'])
def return_output():
  filename = "output.json"
  if os.path.isfile(filename):
    with open(filename, 'r') as f:
      json_data = json.load(f)
    return jsonify(json_data)
  else:
    return "Please wait while the audio is being processed."
@app.route('/example', methods=['GET'])
def return_example():
  filename = "example.json"
  if os.path.isfile(filename):
    with open(filename, 'r') as f:
      json_data = json.load(f)
    return jsonify(json_data)
  else:
    return jsonify({'data':None})

def run_script():
  cmd = ["python", "test.sync.py"]
  subprocess.run(cmd)

if __name__ == '__main__':
  #the_other_process = subprocess.Popen(['python', 'test.sync.py'],shell=True)
  thread = threading.Thread(target=run_script)
  thread.start()
  app.run(debug=True,host='0.0.0.0')
