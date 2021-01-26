import requests
import os
import json

from requests.api import head

from dotenv import load_dotenv

load_dotenv()


class ServerManager:
    api_host = os.environ.get("API_HOST")
    email = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")
    token = None
    refresh = None

    @classmethod
    def obtain_token(cls):
        credentials = {
            "email": cls.email,
            "password": cls.password
        }

        r = requests.post(url=f"{cls.api_host}/token/", json=credentials)
        data = json.loads(r.text)
        return data.get('access')

    @classmethod
    def refresh_token(cls):
        r = requests.post(
            url=f"{cls.api_host}/token/refresh/", json={"refresh": cls.refresh})
        cls.token = json.loads(r.text).get('token')

    @classmethod
    def send_solution(cls, problem_id, file_content):
        token = cls.obtain_token()
        url = f"{cls.api_host}/submit/"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        data = {
            "problem": int(problem_id),
            "language": 1,
            "code": "\n".join(file_content)
        }
        r = requests.post(url=url, json=data, headers=headers)
        response = json.loads(r.text)
        tests = response.get('tests')
        if response.get('exitcode') != 0:
            print("------------------------------")
            print(f"Problem #{problem_id}")
            print(f"Outcome: failed")
        else:
            for test in tests:
                print("------------------------------")
                print(f"Problem #{problem_id}")
                print(f"Outcome: {test.get('outcome')}")
