from flask import Flask, jsonify
import socket

local_hostname = socket.gethostname()
ip_addresses = socket.gethostbyname_ex(local_hostname)[2]


app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message=f"Hello from cluster <{local_hostname}>", ip_addr=f"{ip_addresses}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
