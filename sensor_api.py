from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'sensor_data.json'

@app.route('/update-sensor', methods=['POST'])
def update_sensor():
    try:
        data = request.get_json()
        if data:
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f)
            return jsonify({"status": "success", "message": "Data saved"}), 200
        else:
            return jsonify({"status": "error", "message": "No data provided"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get-sensor', methods=['GET'])
def get_sensor():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            return jsonify(data), 200
        else:
            return jsonify({"ph": 7.0, "tds": 100, "turbidity": 4.0}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
