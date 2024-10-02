from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/yoinkGPT', methods=['POST'])
def yoink_gpt():
    data = request.json  # Get the JSON data from the request
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Process the data as needed
    response = {
        "message": "Data received at yoinkGPT!",
        "received": data
    }
    return jsonify(response), 200

@app.route('/yoinkBG', methods=['POST'])
def yoink_bg():
    data = request.json  # Get the JSON data from the request
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Process the data as needed
    response = {
        "message": "Data received at yoinkBG!",
        "received": data
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
