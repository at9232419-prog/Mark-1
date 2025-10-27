from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET', 'HEAD'])
def home():
    return jsonify({"message": "Your Flask web app is running successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
