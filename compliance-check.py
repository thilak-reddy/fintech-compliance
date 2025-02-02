#!/usr/bin/env python3

import requests
import time
import os

JENKINS_URL = "http://localhost:8080"
JOB_NAME = "compliance-new"
USER = "thilak"
API_TOKEN = "1158c9b17b0afef60a01ea905d8454b1e5"

LOG_DIR = "/Users/thilak_reddy/Desktop/fintech-compliance/compliance_logs"
LOG_FILE = os.path.join(LOG_DIR, "compliance_logs.txt")

def trigger_build():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/build"
    response = requests.post(url, auth=(USER, API_TOKEN))
    if response.status_code == 201:
        print("Build triggered successfully!")
    else:
        print(f"Failed to trigger build: {response.status_code}")
        exit(1)

def get_latest_build():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/buildNumber"
    response = requests.get(url, auth=(USER, API_TOKEN))
    return response.text.strip() if response.status_code == 200 else None

def wait_for_build(build_number):
    while True:
        url = f"{JENKINS_URL}/job/{JOB_NAME}/{build_number}/api/json"
        response = requests.get(url, auth=(USER, API_TOKEN))
        result = response.json().get("result")

        if result:
            print(f"Build completed with status: {result}")
            return result
        print("Waiting for build to complete...")
        time.sleep(5)

def fetch_logs(build_number):
    # Ensure the log directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    url = f"{JENKINS_URL}/job/{JOB_NAME}/{build_number}/consoleText"
    response = requests.get(url, auth=(USER, API_TOKEN))

    with open(LOG_FILE, "w") as log_file:
        log_file.write(response.text)

    print(f"Logs saved to {LOG_FILE}")

if __name__ == "__main__":
    trigger_build()
    build_number = get_latest_build()
    if build_number:
        wait_for_build(build_number)
        fetch_logs(build_number)
