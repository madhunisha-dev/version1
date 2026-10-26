
from flask import Flask, request, render_template_string, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = "assets.json"

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Asset Management System - V3</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            margin: 0;
            padding: 40px 20px;
        }
        .container {
            max-width: 950px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
        }
        h1 { color: #1e3a8a; }
        input, button {
            box-sizing: border-box;
            padding: 10px;
            margin: 5px 0;
        }
        input { width: 100%; }
        button {
            background: #1d4ed8;
            color: white;
            border: 0;
            border-radius: 6px;
            cursor: pointer;
        }
        .delete-button { background: #dc2626; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            border: 1px solid #cbd5e1;
            text-align: left;
        }
        th { background: #dbeafe; }
        .message { color: #15803d; }
        .table-wrap { overflow-x: auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Asset Management System</h1>
        <p>Version 3 - Add, View and Delete Assets</p>

        <h2>Add Asset</h2>
        <form method="POST" action="/add">
            <input name="asset_name" placeholder="Asset name" required>
            <input name="asset_type" placeholder="Asset type" required>
            <input name="location" placeholder="Asset location" required>
            <button type="submit">Add Asset</button>
        </form>

        <p class="message">{{ message }}</p>

        <h2>View Assets</h2>
        <div class="table-wrap">
            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Location</th>
                    <th>Action</th>
                </tr>
                {% for asset in assets %}
                <tr>
                    <td>{{ asset.id }}</td>
                    <td>{{ asset.name }}</td>
                    <td>{{ asset.type }}</td>
                    <td>{{ asset.location }}</td>
                    <td>
                        <form method="POST" action="/delete/{{ asset.id }}"
                              onsubmit="return confirm('Delete this asset?');">
                            <button type="submit" class="delete-button">
                                Delete
                            </button>
                        </form>
                    </td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="5">No assets added yet.</td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </div>
</body>
</html>
"""

def load_assets():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_assets(assets):
    with open(DATA_FILE, "w") as file:
        json.dump(assets, file, indent=4)

@app.route("/")
def home():
    return render_template_string(PAGE, assets=load_assets(), message="")

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
        return render_template_string(
            PAGE, assets=assets, message="All fields are required."
        )

    assets.append(asset)
    save_assets(assets)
    return redirect(url_for("home"))

@app.route("/delete/<int:asset_id>", methods=["POST"])
def delete_asset(asset_id):
    assets = load_assets()
    updated_assets = [a for a in assets if a["id"] != asset_id]

    if len(updated_assets) == len(assets):
        message = "Asset not found."
    else:
        save_assets(updated_assets)
        message = "Asset deleted successfully!"

    return render_template_string(
        PAGE, assets=load_assets(), message=message
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
