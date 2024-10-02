from flask import Flask, request, jsonify
from flask_cors import CORS
from bible_gateway_yoinker import bible_gateway_yoink
from gpt_yoinker import chatgpt_yoink

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/yoinkGPT', methods=['POST'])
def yoink_gpt():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Process the data as needed
    gptResponse = chatgpt_yoink(data['version'], data['book'], data['chapter'], data['verses'])

    response = {
        "message": "Data received at yoinkGPT!",
        "text": gptResponse
    }
    return jsonify(response), 200


@app.route('/yoinkBG', methods=['POST'])
def yoink_bg():
    data = request.json  # Get the JSON data from the request
    if not data:
        return jsonify({"error": "No data provided"}), 400

    print(data)
    bgResponse = bible_gateway_yoink(data['version'], data['book'], data['chapter'], data['verses'])


    if bgResponse is None:
        bgResponse = "No text found."  # Default message or handle the error
        
    # Process the data as needed
    response = {
        "message": "Data received at yoinkBG!",
        "text": bgResponse
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
