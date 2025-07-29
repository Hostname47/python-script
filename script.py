import requests
import time
from requests.auth import HTTPBasicAuth

# === CONFIGURATION ===
JENKINS_URL = "http://localhost:8080"
JOB_NAME = "my-pipeline-job"
USERNAME = "admin"
API_TOKEN = "your-api-token"  # Get this from Jenkins -> your user -> Configure -> API Token
POLL_INTERVAL = 3  # seconds

# === TRIGGER BUILD ===
def trigger_build():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/build"
    response = requests.post(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))
    if response.status_code == 201:
        print("✅ Build triggered.")
    else:
        raise Exception(f"Failed to trigger build: {response.status_code} {response.text}")

# === GET LAST BUILD NUMBER ===
def get_last_build_number():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/api/json"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN)).json()
    return response['lastBuild']['number']

# === POLL BUILD STATUS ===
def wait_for_build_completion(build_number):
    while True:
        url = f"{JENKINS_URL}/job/{JOB_NAME}/{build_number}/api/json"
        response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN)).json()
        building = response['building']
        if not building:
            return response['result']
        print("⏳ Waiting for build to finish...")
        time.sleep(POLL_INTERVAL)

# === MAIN FLOW ===
if __name__ == "__main__":
    print("🚀 Starting Jenkins pipeline test...")
    trigger_build()
    time.sleep(2)  # slight delay to let Jenkins register the new build
    build_number = get_last_build_number()
    print(f"🔍 Monitoring build #{build_number}...")
    result = wait_for_build_completion(build_number)
    if result == "SUCCESS":
        print("✅ Build succeeded.")
    else:
        print(f"❌ Build failed with result: {result}")
