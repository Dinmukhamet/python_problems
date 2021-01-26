from os import walk, getcwd, path
from utils import ServerManager

base_url = getcwd()
problems_path = path.join(base_url, "problems")


_, _, filenames = next(walk(problems_path))

for problem in filenames:
    with open(path.join(problems_path, problem), 'r') as f:
        problem_id = problem.rsplit('_')[0]
        ServerManager.send_solution(problem_id=problem_id, file_content=f.readlines())