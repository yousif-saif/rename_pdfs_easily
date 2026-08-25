from flask import Flask, send_file, render_template, request
from helpers import *
import os
from pathlib import Path
from urllib.parse import quote
from werkzeug.utils import safe_join
import base64

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/view-pdf")
def view_pdf():
    b64_path = request.args.get("id", "")
    try:
        raw_path = base64.b64decode(b64_path).decode("utf-8")
    except Exception:
        raw_path = ""
        
    base_dir = Path(__file__).resolve().parent / "pdfs"
    full_path = safe_join(str(base_dir), raw_path)

    if not full_path or not os.path.isfile(full_path):
        return "File not found", 404

    # Serve as text/plain with no Content-Disposition to completely hide from IDM
    response = send_file(full_path, mimetype="text/plain", as_attachment=False)
    return response


@app.route("/api/pdfs")
def api_pdfs():
    # print("PDFS: ", get_pdfs())
    return {"pdfs": get_pdfs()}


@app.route("/api/rename", methods=["POST"])
def api_rename():
    data = request.json
    old_path = data.get("old_path")
    new_name = data.get("new_name")

    if not old_path or not new_name:
        return {"error": "Missing old_path or new_name"}, 400

    if not new_name.lower().endswith(".pdf"):
        new_name += ".pdf"
        
    base_dir = Path(__file__).resolve().parent / "pdfs"
    old_full_path = safe_join(str(base_dir), old_path)
    
    if not old_full_path or not os.path.isfile(old_full_path):
        return {"error": "File not found"}, 404
        
    new_full_path = Path(old_full_path).parent / new_name
    
    if new_full_path.exists():
        return {"error": "Target file already exists"}, 400
        
    os.rename(old_full_path, new_full_path)
    
    # Return the new relative path
    new_rel_path = new_full_path.relative_to(base_dir)
    return {"new_path": str(new_rel_path).replace("\\", "/")}
if __name__ == "__main__":
    app.run(debug=True, port=9999)
    