from dotenv import load_dotenv
from os import getenv
from flask import Flask, request, jsonify
from http.client import OK , BAD_REQUEST , INTERNAL_SERVER_ERROR
from repository.database import UserDAO , User
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

@app.route("/user",methods=["GET"])
def users():
   # -- forming request
   name = request.args.get("name")
   if name is None or name == "":
      #  -- return error case
       return jsonify({"message" : "invalid request" , "data" : None}), BAD_REQUEST 
   # -- calling service
   collection = UserDAO(uri=db_uri,port=db_port,database_name="FlaskServer",collection_name="users")
   # -- database query
   try:
      result = collection.find_user_by_name(name)
   except:
      return jsonify({"message" : "database connection error", "data" : None}) , INTERNAL_SERVER_ERROR
   collection.close_connection()
   # -- forming response
   if result is None:
      return jsonify({"message" : "forming response error", "data" : None}) , INTERNAL_SERVER_ERROR
   res = jsonify({"message" : "success","data" :result.to_dict()}), OK
   return res
if __name__ == "__main__":
   load_dotenv()
   db_uri = getenv("DB_URI")
   db_port = int(getenv("DB_PORT"))
   
   app.run(port=8080, debug=True, use_reloader=False)