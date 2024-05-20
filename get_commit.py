#!/usr/bin/env python3
"""
Simple python implementation of Most Recent Git Commit for the terminal
"""

from datetime import datetime, timezone
import requests


def get_relative_time(date: datetime):
    """Take a datetime and return its "age" as a string.
    The age can be in second, minute, hour, day, month or year. Only the
    biggest unit is considered, e.g. if it's 2 days and 3 hours, "2 days" will
    be returned.
    Make sure date is not in the future, or else it won't work.
    Original Gist by 'zhangsen' @ https://gist.github.com/zhangsen/1199964
    Original Gist by 'jonlabelle' @
    https://gist.github.com/jonlabelle/7d306575cbbd34b154f87b1853d532cc
    """

    class FormatDelta:  # pylint: disable=too-few-public-methods
        """
        Wrapper around format method to convert datetime to
        relative time string
        """

        def __init__(self, dt: datetime) -> None:
            now = datetime.now(timezone.utc)
            delta = now - dt
            self.day = delta.days
            self.second = delta.seconds
            self.year, self.day = divmod(self.day, 365)
            self.month, self.day = divmod(self.day, 30)
            self.hour, self.second = divmod(self.second, 3600)
            self.minute, self.second = divmod(self.second, 60)

        def format(self):
            """Public method to get the relative time"""
            for period in ["year", "month", "day", "hour", "minute", "second"]:
                num = getattr(self, period)
                if num >= 1:
                    return f"{num} {period}{'s' if num > 1 else ''} ago"
            return "just now"

    return FormatDelta(date).format()


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
