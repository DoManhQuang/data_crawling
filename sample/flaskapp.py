from flask import Flask, redirect, url_for, request
app = Flask(__name__)

@app.route('/login', methods=['POST', 'GET'])
def login():
	name = request.args.get('name')
	return 'hello ' + name



if __name__ == '__main__':
	app.run(debug=True)
