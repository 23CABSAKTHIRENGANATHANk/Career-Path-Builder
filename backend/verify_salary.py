
import requests
import json

url = "http://127.0.0.1:5000/api/analyze-profile"

# Test Case 1: Bangalore
payload_bangalore = {
    "technical_skills": ["JavaScript", "React", "Node.js"],
    "soft_skills": ["Communication"],
    "interests": ["Coding"],
    "city": "Bangalore"
}

# Test Case 2: Remote
payload_remote = {
    "technical_skills": ["JavaScript", "React", "Node.js"],
    "soft_skills": ["Communication"],
    "interests": ["Coding"],
    "city": "Remote"
}

try:
    print("Testing Bangalore...")
    response_blr = requests.post(url, json=payload_bangalore)
    data_blr = response_blr.json()
    salary_blr = data_blr['data']['career_recommendation']['salary_range']
    print(f"Bangalore Salary: {salary_blr}")

    print("\nTesting Remote...")
    response_remote = requests.post(url, json=payload_remote)
    data_remote = response_remote.json()
    salary_remote = data_remote['data']['career_recommendation']['salary_range']
    print(f"Remote Salary: {salary_remote}")

    if salary_blr != salary_remote:
        print("\n✅ SUCCESS: Salary varies by location!")
    else:
        print("\n❌ FAILED: Salary did not change.")

except Exception as e:
    print(f"\n❌ Error: {e}")
