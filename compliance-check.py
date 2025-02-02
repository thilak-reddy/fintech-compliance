#!/usr/bin/env python3

import requests
import time
import os
import json
import logging
from datetime import datetime

JENKINS_URL = "http://localhost:8080"
JOB_NAME = "compliance-new"
USER = "thilak"
API_TOKEN = "1158c9b17b0afef60a01ea905d8454b1e5"

LOG_DIR = "/Users/thilak_reddy/Desktop/fintech-compliance/compliance_logs"
LOG_FILE = os.path.join(LOG_DIR, "compliance_logs.txt")
DETAILED_LOG_FILE = os.path.join(LOG_DIR, "detailed_compliance_report.json")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'compliance_checks.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def analyze_compliance_reports():
    reports = {
        'pci': 'pci_report.json',
        'soc2': 'soc2_report.json'
    }
    
    detailed_report = {
        'timestamp': datetime.now().isoformat(),
        'overall_status': 'PASS',
        'failures': [],
        'summary': {}
    }

    for compliance_type, report_file in reports.items():
        try:
            with open(report_file, 'r') as f:
                report_data = json.load(f)
                
            failed_controls = [
                control for control in report_data.get('controls', [])
                if control.get('status') == 'failed'
            ]
            
            if failed_controls:
                detailed_report['overall_status'] = 'FAIL'
                for control in failed_controls:
                    failure = {
                        'compliance_type': compliance_type,
                        'control_id': control.get('id'),
                        'title': control.get('title'),
                        'failure_message': control.get('message'),
                        'impact': control.get('impact')
                    }
                    detailed_report['failures'].append(failure)
                    logger.error(f"Compliance failure: {compliance_type} - {control.get('id')}: {control.get('title')}")

            detailed_report['summary'][compliance_type] = {
                'total_controls': len(report_data.get('controls', [])),
                'failed_controls': len(failed_controls),
                'passed_controls': len(report_data.get('controls', [])) - len(failed_controls)
            }
            
        except Exception as e:
            logger.error(f"Error processing {compliance_type} report: {str(e)}")
            detailed_report['failures'].append({
                'compliance_type': compliance_type,
                'error': str(e)
            })

    # Save detailed report
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(DETAILED_LOG_FILE, 'w') as f:
        json.dump(detailed_report, f, indent=2)
    
    return detailed_report

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
            logger.info(f"Build completed with status: {result}")
            if result == 'SUCCESS':
                detailed_report = analyze_compliance_reports()
                logger.info(f"Compliance check summary: {json.dumps(detailed_report['summary'], indent=2)}")
                if detailed_report['failures']:
                    logger.warning("Some compliance checks failed. Check detailed_compliance_report.json for more information.")
            return result
        logger.info("Waiting for build to complete...")
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
