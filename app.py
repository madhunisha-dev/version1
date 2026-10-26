from flask import Flask, request, render_template_string
import json
import os

app = Flask(__name__)
DATA_FILE = "assets.json"

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Asset Management System - V1</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            margin: 0;
            padding: 40px 20px;
        }
        .container {
            max-width: 500px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
        }
        h1 { color: #1e3a8a; }
        input, button {
            box-sizing: border-box;
            width: 100%;
            padding: 12px;
            margin: 10px 0;
        }
        button {
            background: #1d4ed8;
            color: white;
            border: 0;
            border-radius: 6px;
            cursor: pointer;
        }
        .message { color: #15803d; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Asset Management System</h1>
        <p>Version 1 - Add Asset</p>
        <form method="POST" action="/add">
            <input name="asset_name" placeholder="Asset name" required>
            <input name="asset_type" placeholder="Asset type" required>
            <input name="location" placeholder="Asset location" required>
            <button type="submit">Add Asset</button>
        </form>
        <p class="message">{{ message }}</p>
    </div>
</body>
</html>
"""

def load_assets():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

@app.route("/")
def home():
    return render_template_string(PAGE, message="")

@app.route("/add", methods=["POST"])
def add_asset():
    assets = load_assets()
    asset = {
        "id": max([a["id"] for a in assets], default=0) + 1,
        "name": request.form["asset_name"].strip(),
        "type": request.form["asset_type"].strip(),
        "location": request.form["location"].strip()
    }

    if not all([asset["name"], asset["type"], asset["location"]]):
        return render_template_string(PAGE, message="All fields are required.")

    assets.append(asset)
    with open(DATA_FILE, "w") as file:
        json.dump(assets, file, indent=4)

    return render_template_string(PAGE, message="Asset added successfully!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
