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


def fix_date(date):
    date = date.split(",")[0]
    return date.replace(' ', '.') \
        .replace('янв', '01') \
        .replace('фев', '02') \
        .replace('мар', '03') \
        .replace('апр', '04') \
        .replace('май', '05') \
        .replace('июн', '06') \
        .replace('июл', '07') \
        .replace('авг', '08') \
        .replace('сен', '09') \
        .replace('окт', '10') \
        .replace('ноя', '11') \
        .replace('дек', '12')


@app.route('/build', methods=['POST'])
def build_predictions():
    req = request.get_json(force=True)
    req["arrival_date"] = fix_date(req["arrival_date"])
    req["return_date"] = fix_date(req["return_date"])
    res = build.build(req)
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
    app.run(host="0.0.0.0", port=5000, debug=True)
