import argparse
import sys
import os
import requests

def test_api(cv_path, job_path, url="http://localhost:8000/api/analyze"):
    if not os.path.exists(cv_path):
        print(f"Error: CV file not found at {cv_path}")
        return
    if not os.path.exists(job_path):
        print(f"Error: Job description file not found at {job_path}")
        return

    print(f"Testing API at {url}")
    print(f"CV: {cv_path}")
    print(f"Job: {job_path}")

    try:
        with open(job_path, 'r', encoding='utf-8') as f:
            job_description = f.read()
    except Exception as e:
        print(f"Error reading job description: {e}")
        return

    files = {
        'cv': open(cv_path, 'rb')
    }
    data = {
        'job_description': job_description
    }

    try:
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            print("\n✅ Success! Analysis result:")
            print("-" * 50)
            print(response.json())
            print("-" * 50)
        else:
            print(f"\n❌ Error {response.status_code}:")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error: Is the backend running on http://localhost:8000?")
    
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
    
    finally:
        files['cv'].close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the RH AI Agent API")
    parser.add_argument("--cv", required=True, help="Path to CV file (PDF, DOCX, TXT)")
    parser.add_argument("--job", required=True, help="Path to Job Description file (TXT)")
    parser.add_argument("--url", default="http://localhost:8000/api/analyze", help="API Endpoint URL")

    args = parser.parse_args()
    test_api(args.cv, args.job, args.url)
