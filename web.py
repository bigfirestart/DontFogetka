from flask import Flask, request, Response
import json
import save, build

app = Flask(__name__)


def update_response(response: Response):
    # Access-Control-Allow-Origin: http://siteA.com
    # Access-Control-Allow-Methods: GET, POST, PUT
    # Access-Control-Allow-Headers: Content-Type
    # resp.set('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    response.headers.extend({
        "Access-Control-Allow-Origin": "http://*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, OPTION",
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
    })
    return response


@app.route('/build', methods=['POST'])
def build_predictions():
    res = build.build(request.get_json(force=True))
    return update_response(
        Response(json.dumps(res, ensure_ascii=False), mimetype='application/json')
    )


@app.route('/save', methods=['POST'])
def save_predictions():
    response = save.save(request.json)
    return update_response(
        Response("ok")
    )


if __name__ == '__main__':
    app.run()
