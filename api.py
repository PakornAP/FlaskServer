from flask import Flask, request, jsonify
from http.client import OK , BAD_REQUEST
from services.service import Helloname
app = Flask(__name__)

# -- create route (controller)
@app.route("/hello", methods=["GET"])
def hello():
   # -- forming request
   name = request.args.get("name")
   # -- handling request
   if name is None or name == "":
      #  -- return error case
       return jsonify({"message" : "invalid request" , "data" : None}), BAD_REQUEST 
   # -- calling service
   get_res = Helloname(name)
   # -- forming response
   res = jsonify({"message" : "success","data" : get_res}), OK
   return res


if __name__ == "__main__":
    app.run(port=8080, debug=True, use_reloader=False)