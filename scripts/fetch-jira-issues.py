import os
import pandas as pd
import requests

# JIRA API credentials
JIRA_URL = 'https://ce-platform.atlassian.net/rest/api/3/search'
API_TOKEN = os.getenv('JIRA_API_TOKEN')

# Function to make a JIRA API request
def fetch_issues(start_at, max_results=100):
    headers = {
        'Accept': 'application/json',
        'Authorization': API_TOKEN,
    }
    
    params = {
        'startAt': start_at,
        'maxResults': max_results,
        'jql': 'project = UNBO ORDER BY created DESC',
    }
    
    try:
        response = requests.get(JIRA_URL, headers=headers, params=params)
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print("Error fetching issues:", e)
        return None

# Function to gather all issues
def gather_all_issues():
    all_issues = []
    start_at = 0
    max_results = 100

    while True:
        response_data = fetch_issues(start_at, max_results)
        
        if response_data is None:
            break
        
        issues = response_data.get('issues', [])
        all_issues.extend(issues)
        
        if len(issues) < max_results:
            break
        
        start_at += max_results
    
    return all_issues

# Fetch all issues
issues = gather_all_issues()

# Process and write issues to CSV
def write_issues_to_csv(issues, file_name='jira-issues.csv'):
    issues_data = []
    
    for issue in issues:
        issue_data = {
            'id': issue['id'],
            'key': issue['key'],
            'summary': issue['fields']['summary'],
            # 'status': issue['fields']['status']['name'],
            # 'assignee': issue['fields'].get('assignee', {}).get('displayName', 'Unassigned'),
            # 'created': issue['fields']['created'],
            # Add more fields as needed
        }
        issues_data.append(issue_data)
    
    df = pd.DataFrame(issues_data)
    df.to_csv(file_name, index=False)

# Write issues to CSV
write_issues_to_csv(issues)