#!/usr/bin/env python3
"""
Simple python implementation of Most Recent Git Commit for the terminal
"""

from datetime import datetime, timezone
import requests


def get_relative_time(date: datetime) -> str:
    """Take a datetime and return its "age" as a string.
    The age can be in second, minute, hour, day, month or year. Only the
    biggest unit is considered, e.g. if it's 2 days and 3 hours, "2 days" will
    be returned.
    Make sure date is not in the future, or else it won't work.
    Original Gist by 'zhangsen' @ https://gist.github.com/zhangsen/1199964
    Original Gist by 'jonlabelle' @
    https://gist.github.com/jonlabelle/7d306575cbbd34b154f87b1853d532cc
    """

    now = datetime.now(timezone.utc)
    delta = now - date
    day = delta.days
    second = delta.seconds
    year, day = divmod(day, 365)
    month, day = divmod(day, 30)
    hour, second = divmod(second, 3600)
    minute, second = divmod(second, 60)
    nums = [year, month, day, hour, minute, second]

    for num, period in zip(nums, ["year", "month", "day", "hour", "minute", "second"]):
        if num >= 1:
            return f"{num} {period}{'s' if num > 1 else ''} ago"
    return "just now"


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
    date = data["commit"]["author"]["date"]
    return {
        "repo": repo,
        "message": data["commit"]["message"],
        "date": f"{date} ({get_relative_time(datetime.fromisoformat(date))})",
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
