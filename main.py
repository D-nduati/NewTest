import os
import random
from datetime import datetime, timedelta

# CONFIGURATION - SET THESE!
GITHUB_EMAIL = "mwakidavis89@gmail.com"  # Must match verified GitHub email
REPO_BRANCH = "main"  # Must be your default branch

def verify_settings():
    # Verify email configuration
    current_email = os.popen('git config user.email').read().strip()
    if current_email != GITHUB_EMAIL:
        print(f"✖ Email mismatch! Git: '{current_email}' ≠ GitHub: '{GITHUB_EMAIL}'")
        os.system(f'git config user.email "{GITHUB_EMAIL}"')
        print("✓ Fixed: Updated git email config")
    
    # Verify branch
    current_branch = os.popen('git branch --show-current').read().strip()
    if current_branch != REPO_BRANCH:
        print(f"✖ Wrong branch! Current: '{current_branch}' ≠ Required: '{REPO_BRANCH}'")
        os.system(f'git checkout -B {REPO_BRANCH}')
        print("✓ Fixed: Switched to correct branch")

def make_qualified_commits():
    verify_settings()
    
    # Initialize tracking file
    if not os.path.exists('.contributions'):
        with open('.contributions', 'w') as f:
            f.write('BEGIN\n')
        os.system('git add .contributions')
        os.system(f'GIT_AUTHOR_DATE="2023-01-01 12:00:00" GIT_COMMITTER_DATE="2023-01-01 12:00:00" git commit -m "Initial commit"')

    # Generate commits
    for day in (datetime(2023, 1, 1) + timedelta(n) for n in range(200)):
        if day.year != 2023:
            continue
            
        # Skip some days realistically
        if day.weekday() >= 5 and random.random() < 0.7:  # 70% skip weekends
            continue
        if random.random() < 0.2:  # 20% skip weekdays
            continue
            
        # Make 1-4 commits per day
        for _ in range(random.randint(1, 4)):
            # Random time (80% during work hours)
            hour = random.randint(9, 17) if random.random() < 0.8 else random.randint(0, 23)
            commit_time = day.replace(
                hour=hour,
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
            
            # Write unique content
            with open('.contributions', 'a') as f:
                f.write(f"{commit_time.isoformat()}\n")
            
            # Make qualifying commit
            git_date = commit_time.strftime('%Y-%m-%d %H:%M:%S')
            os.system('git add .contributions')
            os.system(f'GIT_AUTHOR_DATE="{git_date}" GIT_COMMITTER_DATE="{git_date}" git commit -m "contribution: {git_date}"')

    # Final push
    os.system(f'git push -u origin {REPO_BRANCH}')

if __name__ == '__main__':
    make_qualified_commits()
    print("""
    ✓ Commits generated successfully!
    → Wait 10-30 minutes for GitHub to update graphs
    → Verify at: https://github.com/users/david/contributions
    """)