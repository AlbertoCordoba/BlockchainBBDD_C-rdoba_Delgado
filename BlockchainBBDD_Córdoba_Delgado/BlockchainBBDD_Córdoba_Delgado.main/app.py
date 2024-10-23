from flask import Flask,request, render_template
import socket


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')




@app.route('/', methods=['POST'])
def send():
    message = request.form['message']
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8000))
    sock.send(message.encode())
    sock.close()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)