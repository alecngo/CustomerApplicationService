from flask import jsonify
from dotenv import load_dotenv
from app import app
import redis 

load_dotenv()

r = redis.Redis(host="redis", port=6379)

@app.route('/')
def index():
    return jsonify({"message": "Hello, World!"})

@app.route("/hits")
def read_root():
    r.incr("hits")
    hit_count = r.get("hits").decode("utf-8")  # Decode bytes to string
    return jsonify({"Number of hits": hit_count})

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=8001)