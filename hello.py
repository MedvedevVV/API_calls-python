from flask import Flask, request
import os
application = Flask(__name__)


@application.route("/" , methods=['POST', 'GET'])
def hello():
   if request.method == 'POST':
      request.environ['CONTENT_TYPE'] = 'application/something_Flask_ignores'
      data = request.data
      data = data.decode('utf-8')
      rest = str(data)
      if 'Success' in rest:
         file = open("REST.txt", "w")
         file.write(rest)
         file.close()
         os.system("python script.py")
         return('')
   else:
      return "<h1 style='color:black'>Ошибка доступа</h1>"

if __name__ == "__main__":
   application.run(host='0.0.0.0', port = '5000')
    
