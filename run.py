from os import walk, getcwd, path
from utils import ServerManager
import sys

args = sys.argv[1:]
base_url = getcwd()
problems_path = path.join(base_url, "problems")

if not args:
    _, _, filenames = next(walk(problems_path))
    for problem in filenames:
        with open(path.join(problems_path, problem), 'r', encoding='utf-8') as f:
            problem_id = problem.rsplit('_')[0]
            ServerManager.send_solution(
                problem_id=problem_id, file_content=f.readlines())
else:
    for problem_id in args:
        problem = f"{problem_id}_problem.py"
        with open(path.join(problems_path, problem), 'r', encoding='utf-8') as f:
            ServerManager.send_solution(
                problem_id=problem_id, file_content=f.readlines())
