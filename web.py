from flask import Flask, request, Response
import json
import save, build

app = Flask(__name__)


@app.route('/build', methods=['POST'])
def build_predictions():
    res = build.build(request.json)
    return Response(json.dumps(res, ensure_ascii=False), mimetype='application/json')


@app.route('/save', methods=['POST'])
def save_predictions():
    response = save.save(request.json)
    return "ok"


if __name__ == '__main__':
    app.run()
