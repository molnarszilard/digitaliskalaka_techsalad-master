from flask import Flask
app = Flask(__name__)
from image_saver import *

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/dolgozz')
def valami_nev():
   record()
   #crop()
   result=classify()
   return result


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)
