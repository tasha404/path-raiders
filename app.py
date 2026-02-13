@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    image_url = None
    
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

        import base64
        image_url = base64.b64encode(img.getvalue()).decode()

        plt.close(fig)

    return render_template(
        "index.html",
        problems=MAZES.keys(),
        result=result,
        image=image_url
    )
