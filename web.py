from flask import Flask , request
app = Flask(__name__)

@app.route('/build', methods=['POST'])
def build():
    print(request.json)
    #returns listJson 1
    return request.json
@app.route('/save', methods=['POST'])
def save():
    #gets listJson 2
    return 0

if __name__ == '__main__':
    app.run()