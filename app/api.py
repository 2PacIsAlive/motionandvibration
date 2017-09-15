from flask import Flask, jsonify, render_template, request
import inspect
from collections import defaultdict


app = application = Flask("motionandvibration", static_url_path='')
calls = defaultdict(lambda: 0)


@app.route("/", methods=["GET"])
def index():
    calls[inspect.stack()[0][3]] += 1
    return render_template('index.html'), 200


@app.route("/cryptopticon/healthz", methods=["GET"])
def healthz():
    calls[inspect.stack()[0][3]] += 1
    return Health(calls) \
               .to_json(), 200


class Health(object):
    def __init__(self, calls):
        self.calls = calls

    def to_json(self):
        return jsonify({
            "requestsServed": {
                "index": self.calls["index"],
                "healthz": self.calls["healthz"]
            },
            "status": "healthy"
        })


if __name__ == '__main__':
    app.run(debug=True)
