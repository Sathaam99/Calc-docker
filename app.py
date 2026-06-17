from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Serve the HTML GUI on the base URL
@app.route('/')
def home():
    return render_template('index.html')

# The Calculator API
@app.route('/calculate', methods=['GET'])
def calculate():
    op = request.args.get('op')
    
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
    except ValueError:
        return jsonify(error="Inputs must be numbers"), 400

    if op == 'add':
        return jsonify(operation="addition", result=a + b)
    elif op == 'sub':
        return jsonify(operation="subtraction", result=a - b)
    elif op == 'mul':
        return jsonify(operation="multiplication", result=a * b)
    elif op == 'div':
        if b == 0:
            return jsonify(error="Division by zero is not allowed"), 400
        return jsonify(operation="division", result=a / b)
    else:
        return jsonify(error="Invalid operation. Use add, sub, mul, or div"), 400

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify(status="healthy")

if __name__ == '__main__':
    # Binds to 0.0.0.0 and runs on port 5060 to match the Dockerfile EXPOSE directive
    app.run(host='0.0.0.0', port=5060)
