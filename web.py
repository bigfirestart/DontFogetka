from flask import Flask, request
import json
import save
app = Flask(__name__)

@app.route('/build', methods=['POST'])
def build():
    list = json.dumps(request.json)
    #returns listJson 1
    return list

@app.route('/save', methods=['POST'])
def saveList():
    response = save.save(request.json)
    return "ok"

if __name__ == '__main__':
    app.run()