import requests
import os
import json
import sys

from requests.api import head

from dotenv import load_dotenv

load_dotenv()


class ServerManager:
    api_host = os.environ.get("API_HOST")
    email = os.environ.get("EMAIL")
    password = os.environ.get("PASSWORD")

    @classmethod
    def obtain_token(cls):
        credentials = {
            "email": cls.email,
            "password": cls.password
        }
        if None in [cls.api_host, cls.email, cls.password]:
            print("Run of this file has failed.")
            print("The possible reasons why:")
            print("1. You've forgot to create .env file with values")
            print("2. You've forgot to add your values into the file")
            print("3. The server is not responding")
            sys.exit(1)

        r = requests.post(url=f"{cls.api_host}/token/", json=credentials)
        data = json.loads(r.text)
        return data.get('access')

    @classmethod
    def get_results(cls, submission_number):
        token = cls.obtain_token()
        headers = {
            "Authorization": f"Bearer {token}"
        }
        r = requests.get(
            f"{cls.api_host}/submissions/{submission_number}", headers=headers)
        response = json.loads(r.text)
        if response.get('status') == 'Pending':
            return cls.get_results(submission_number)
        return response

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
            "code": "".join(file_content)
        }
        r = requests.post(url=url, json=data, headers=headers)
        # response = json.loads(r.text)
        # report = cls.get_results(response.get(
        #     'submission_number')).get('report')
        # tests = report.get('tests')
        # if report.get('exitcode') != 0:
        #     print("------------------------------")
        #     print(f"Problem #{problem_id}")
        #     print(f"Outcome: failed")
        # else:
        #     for test in tests:
        #         print("------------------------------")
        #         print(f"Problem #{problem_id}")
        #         print(f"Outcome: {test.get('outcome')}")
