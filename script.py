import os
import sys
import pandas as pd
import shutil
import re
import subprocess
import openpyxl

def extract_name(email):
    """Extracts first and last name from the email format x_y.z@q.d"""
    match = re.match(r".*_(\w+)\.(\w+)@", email)
    if match:
        return match.group(1).capitalize(), match.group(2).capitalize()
    return None, None

def process_grading(grader_name, test_file_path, team_grading_path):
    # Read the team grading file which includes details about graders and teams
    df = pd.read_excel(team_grading_path)

    # Filter rows only for the given grader name - Feel free to remove it if you want to help other TAs :D
    filtered_df = df[df["Grader Name"] == grader_name]

    # Get unique groups
    unique_groups = filtered_df["group_name"].unique()

    teams_path = os.path.join(os.getcwd(), 'teams')
    os.makedirs(teams_path, exist_ok=True)

    for group in unique_groups:
        # Get relevant group members
        group_members = filtered_df[filtered_df["group_name"] == group] 

        # Extract repo URL and convert HTTP to SSH
        repo_url_http = group_members["student_repository_url"].iloc[0]
        repo_url_ssh = repo_url_http.replace("https://", "git@").replace("/", ":", 1)

        # Define the directory name for the cloned repo
        repo_name = repo_url_http.split("/")[-1].replace(".git", "")
        repo_path = os.path.join(teams_path, repo_name)

        # Clone the repository using SSH
        if not os.path.exists(repo_path):  # Avoid cloning if the repo already exists
            subprocess.run(["git", "clone", repo_url_ssh], cwd=teams_path)

        # Ensure the repo was cloned successfully
        if not os.path.exists(repo_path):
            print(f"Failed to clone repository: {repo_url_ssh}")
            continue

        # Copy the test file to the cloned repo
        dest_test_file = os.path.join(repo_path, os.path.basename(test_file_path))
        shutil.copy(test_file_path, dest_test_file)

        # Extract student names
        students = []
        for email in group_members["roster_identifier"]:
            first_name, last_name = extract_name(email)
            if first_name and last_name:
                students.append(f"{first_name} {last_name}")

        # Get grader email
        grader_email = group_members["Grader Email"].iloc[0]

        # Fill the test file
        test_df = pd.read_excel(dest_test_file, header=None)
        mapping = {
            "Team Name:": group,
            "Student 1:": students[0] if len(students) > 0 else "?",
            "Student 2:": students[1] if len(students) > 1 else "?",
            "Grader Name:": grader_name,
            "Grader Email:": grader_email
        }

        for i in range(len(test_df)):
            if test_df.iloc[i, 0] in mapping:
                test_df.iloc[i, 1] = mapping[test_df.iloc[i, 0]]

        test_df.to_excel(dest_test_file, index=False, header=False)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <Grader Name> <test_file.xlsx> <team_grading.xlsx>")
        sys.exit(1)

    grader_name = sys.argv[1]
    test_file_path = sys.argv[2]
    team_grading_path = sys.argv[3]

    process_grading(grader_name, test_file_path, team_grading_path)
