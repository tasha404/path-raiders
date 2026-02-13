from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import io

from bfs import bfs
from dfs import dfs
from astar import astar
from mazeconf import MAZES
from visualization import draw_maze

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    image = None
    
    problem = list(MAZES.keys())[0]
    algorithm = "BFS"

    if request.method == "POST":
        problem = request.form.get("problem")
        algorithm = request.form.get("algorithm")

        maze_data = MAZES[problem]
        maze = maze_data["maze"]
        start = maze_data["start"]
        goal = maze_data["goal"]

        if algorithm == "BFS":
            result = bfs(maze, start, goal)
        elif algorithm == "DFS":
            result = dfs(maze, start, goal)
        else:
            result = astar(maze, start, goal)

        fig = draw_maze(maze, start, goal, result["path"] if result["success"] else None)
        img = io.BytesIO()
        fig.savefig(img, format="png")
        img.seek(0)
        image = img
        plt.close(fig)

        return send_file(image, mimetype="image/png")

    return render_template("index.html", problems=MAZES.keys())

if __name__ == "__main__":
    app.run()
