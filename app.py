from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

TASKS = []

HTML = """<!DOCTYPE html>
<html>
<head><title>ForgeAgent Demo</title></head>
<body>
    <h1>Task List</h1>
    <ul id="tasks"></ul>
    <script>
        fetch('/api/tasks')
            .then(r => r.json())
            .then(data => {
                const ul = document.getElementById('tasks');
                data.tasks.forEach(t => {
                    const li = document.createElement('li');
                    li.textContent = t;
                    ul.appendChild(li);
                });
            });
    </script>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/tasks")
def get_tasks():
    return jsonify({"tasks": TASKS, "count": len(TASKS)})


@app.route("/api/tasks", methods=["POST"])
def add_task():
    from flask import request
    data = request.get_json() or {}
    title = data.get("title", "")
    if title:
        TASKS.append(title)
        return jsonify({"status": "ok", "task": title}), 201
    return jsonify({"error": "title is required"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
