function getRelativeTime(timestamp) {
    const DAY_MILLISECONDS = 1000 * 60 * 60 * 24;
    const rtf = new Intl.RelativeTimeFormat('en', {
        numeric: 'auto',
    });
    const daysDifference = Math.round(
        (timestamp - new Date().getTime()) / DAY_MILLISECONDS,
    );

    return rtf.format(daysDifference, 'day');
}
async function get_most_recent_repo(user) {
    const url = `https://api.github.com/users/${user}/repos?per_page=100`;
    return fetch(url)
        .then(async response => {
            data = await response.json();
            if (!response.ok || data.length === 0) {
                return [{name: "repo_fetch_failed"}];
            }
            return data;
        })
        .then(data => {
            data.sort((a, b) => new Date(b.pushed_at) - new Date(a.pushed_at));
            return data[0].name;
        })
        .catch(error => console.log('There was a problem with the fetch operation: ' + error.message));
}
async function get_most_recent_commit(user) {
    const repo = await get_most_recent_repo(user)
    const url = `https://api.github.com/repos/${user}/${repo}/commits`;
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                return [{
                    commit: {
                        message: "Fetching commits failed",
                        author: {
                            date: new Date().toISOString(),
                        }
                    },
                    html_url: "https://mecaneer23.github.io/most-recent-git-commit",
                    sha: "Try again"
                }];
            }
            return response.json();
        })
        .then(data => {
            return {
                repo: repo,
                message: data[0].commit.message,
                date: data[0].commit.author.date,
                url: data[0].html_url,
                sha: data[0].sha,
            };
        })
        .catch(error => console.log('There was a problem with the fetch operation: ' + error.message));
}