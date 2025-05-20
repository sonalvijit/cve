from flask import Flask, request, make_response

app = Flask(__name__)

@app.route("/")
def index():
     q = request.args.get("q", "default")
     reponse = make_response("Check the headers!")
     reponse.headers["X-Injected"] = q
     return reponse

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)