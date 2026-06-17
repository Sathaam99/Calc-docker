from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['GET'])
def calculate():
    # Example usage: http://localhost:5000/calculate?op=add&a=5&b=10
    op = request.args.get('op')
    a = float(request.args.get('a', 0))
    b = float(request.args.get('b', 0))

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

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify(status="healthy")

if __name__ == '__main__':
    # Binds to 0.0.0.0 so it's accessible outside the container
    app.run(host='0.0.0.0', port=5000)
