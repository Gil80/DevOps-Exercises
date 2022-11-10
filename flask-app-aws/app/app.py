# Note 1: The use of `import os` is done to validate that the LB is actually
# load balancing by printing the app name each time you refresh the page.
# uncomment the `import os` and `return os.environ["my_var"]` for validation.


from flask import Flask, jsonify
import socket


app = Flask(__name__)
@app.route("/", methods=["GET"])
def get_my_ip():
    return jsonify(socket.gethostbyname(socket.gethostname())), 200
    #return os.environ["my_var"]

app.run(host="0.0.0.0", port=5000, debug=True)

#print(os.os.environ["my_var"])