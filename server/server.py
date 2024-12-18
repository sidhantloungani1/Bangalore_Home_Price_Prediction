from flask import Flask, request, jsonify
import util
app = Flask(__name__)

@app.route('/get_location_names')
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({'estimated_price': price})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print("Error in Prediction:", e)
        return jsonify({'error': str(e)})


if __name__ == "__main__":
    print("starting python flask server for BHP")
    util.load_saved_artifacts()
    app.run(debug=True, host='127.0.0.1', port=5000)
