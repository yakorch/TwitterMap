from flask import Flask, render_template, request
import createweb
app = Flask(__name__)

#@app.route('/')
#def hello_world():
#    return 'Hello from Flask!'

@app.route('/')
def map_func():
 return render_template("index.html")

@app.route("/redirecting", methods=["POST"])
def redirecting():
    if request.method == "POST":
        createweb.main(request.form["name"])
        return render_template("twitter_friends.html")
