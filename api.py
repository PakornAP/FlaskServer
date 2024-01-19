from dotenv import load_dotenv
from os import getenv , path
import cv2
from flask import Flask, request, jsonify
from http.client import OK , BAD_REQUEST , INTERNAL_SERVER_ERROR
from repository.database import UserDAO , User
from services.service import Helloname , MaskDetection
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
def getuser():
   # -- forming request
   name = request.args.get("name")
   if name is None or name == "":
      #  -- return error case
       return jsonify({"message" : "invalid request" , "data" : None}), BAD_REQUEST 
   # -- database repository
   collection = UserDAO(uri=db_uri,port=db_port,database_name="FlaskServer",collection_name="users")
   try:
      result = collection.find_user_by_name(name)
   except:
      return jsonify({"message" : "database process error", "data" : None}) , INTERNAL_SERVER_ERROR
   collection.close_connection()
   # -- forming response
   if result is None:
      return jsonify({"message" : "forming response error", "data" : None}) , INTERNAL_SERVER_ERROR
   res = jsonify({"message" : "success","data" :result.to_dict()}), OK
   return res

@app.route("/user", methods=["PUT"])
def putuser():
   # -- forming request
   keys = ["name" , "age", "feel","filepath","ismask"]
   for k in keys:
      if k not in request.get_json():
         return jsonify({"message" : f"invalid request missing key {k}" , "data" : None}), BAD_REQUEST
   name = request.json["name"]
   age = int(request.json["age"])
   feel = request.json["feel"]
   filepath = request.json["filepath"]
   ismask = bool(request.json["ismask"])
   # -- database repository
   user = User(name,age,feel,filepath,ismask)
   collection = UserDAO(uri=db_uri,port=db_port,database_name="FlaskServer",collection_name="users")
   try:
      result = collection.insert_user(user)
      print(result)
   except:
      return jsonify({"message" : "insert to database error", "data" : str(result)}) , INTERNAL_SERVER_ERROR
   collection.close_connection()
   return jsonify({"message" : "insert success","data" :str(result)}), OK

@app.route("/ismask",methods=["POST"])
def ismask():
   # -- forming request
   filepath = request.json["filepath"]
   if request is None or filepath is None or not path.exists(filepath) :
      #  -- return error case
       return jsonify({"message" : "invalid request" , "data" : None}), BAD_REQUEST 
   try:
      image = cv2.imread(filepath)
      image = cv2.resize(image,(224,224))
      isMask = MaskDetection(image)
   except:
      return jsonify({"message" : "service ismask error", "data" : None}) , INTERNAL_SERVER_ERROR
   # -- forming response
   if isMask is None:
      return jsonify({"message" : "forming response error", "data" : None}) , INTERNAL_SERVER_ERROR
   res = jsonify({"message" : "success","ismask" :isMask}), OK
   return res

# -- main section
if __name__ == "__main__":
   load_dotenv()
   db_uri = getenv("DB_URI")
   db_port = int(getenv("DB_PORT"))
   print(f"URI {db_uri} PORT {db_port}")
   app.run(host="0.0.0.0",port=8080, debug=True, use_reloader=False)