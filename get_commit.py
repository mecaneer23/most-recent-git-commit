#!/usr/bin/env python3
"""
Simple python implementation of Most Recent Git Commit for the terminal
"""

import requests


def get_most_recent_repo(user: str) -> str:
    """Get a user's most recently updated repository on GitHub"""
    return sorted(
        requests.get(f"https://api.github.com/users/{user}/repos?per_page=100").json(),
        key=lambda obj: obj["pushed_at"],
        reverse=True,
    )[0]["name"]


def get_most_recent_commit(user: str) -> dict[str, str]:
    """Get the most recent commit for a given user"""
    repo = get_most_recent_repo(user)
    data = requests.get(f"https://api.github.com/repos/{user}/{repo}/commits").json()[0]
    return {
        "repo": repo,
        "message": data["commit"]["message"],
        "date": data["commit"]["author"]["date"],
        "url": data["html_url"],
        "sha": data["sha"],
    }


def main() -> None:
    """Entry point"""
    user = input("Please enter a github username: ")
    print("Fetching most recent commit...")
    for name, data in get_most_recent_commit(user).items():
        print(f"{name.capitalize()}: {data}")


if __name__ == "__main__":
    main()
