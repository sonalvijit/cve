from flask import Flask, request, jsonify
from urllib.parse import urlparse

app = Flask(__name__)

# Simulated cache (vulnerable)
cache = {}

# Fake product database
products = {
    "victim123": {"name": "Victim's Product", "price": "$50"},
    "attacker666": {"name": "Attacker's Product", "price": "$1"}
}

@app.route('/fetch_product')
def fetch_product():
    # Get the product URL from query
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing url parameter"}), 400

    # VULNERABLE CACHE: using raw URL as cache key without normalization
    if url in cache:
        return jsonify({"cached": True, "data": cache[url]})

    # Extract product ID from the URL (naive parser)
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")
    
    # Assume URL like /dp/<product_id>
    if "dp" in path_parts:
        product_id_index = path_parts.index("dp") + 1
        if product_id_index < len(path_parts):
            product_id = path_parts[product_id_index]
        else:
            return jsonify({"error": "Invalid URL"}), 400
    else:
        return jsonify({"error": "Invalid Amazon URL"}), 400

    # Fetch product data (simulate database lookup)
    product_data = products.get(product_id, {"name": "Unknown Product", "price": "N/A"})

    # Cache it
    cache[url] = product_data

    return jsonify({"cached": False, "data": product_data})

if __name__ == '__main__':
    app.run(debug=True)
