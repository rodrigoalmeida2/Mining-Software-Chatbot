import os
import asyncio
import time
from script.helpers import find_and_convert_in_dir
from github import Github
from github.Commit import Commit
from pydriller import Repository
from urllib.parse import urlparse
import json
from datetime import datetime


def handle_commit(obj):
    if isinstance(obj, Commit):
        return obj.sha
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


def extract_repo_name_from_url(url):
    path = urlparse(url).path
    return path.strip("/")


def extract_repository_info(repo):
    return {
        "url": repo.url,
        # "path": repo.get_path,
        "description": repo.description,
        "homepage": repo.homepage,
        "branches": [branch.name for branch in repo.get_branches()],
        "tags": [tag.name for tag in repo.get_tags()],
        "languages": [language for language in repo.get_languages()],
    }


def extract_commit_info(commit):
    return {
        "hash": commit.hash,
        "message": commit.msg,
        "parents": commit.parents,
        "merge": commit.merge,
        "author": {
            "name": commit.author.name,
            "email": commit.author.email,
            "date": commit.author_date.isoformat(),
        },
        "committer": {
            "name": commit.committer.name,
            "email": commit.committer.email,
            "date": commit.committer_date.isoformat(),
        },
        "modified_files": [],
    }


def extract_modification_info(modification):
    return {
        "old_path": modification.old_path,
        "new_path": modification.new_path,
        "filename": modification.filename,
        "change_type": modification.change_type.name,
        #"diff": modification.diff,
        # "diff_parsed": modification.diff_parsed,
        "added_lines": modification.added_lines,
        "deleted_lines": modification.deleted_lines,
        #"source_code": modification.source_code,
        #"source_code_before": modification.source_code_before,
        #"methods": [method.name for method in modification.methods],
        #"methods_before": [method.name for method in modification.methods_before],
        #"changed_methods": [method.name for method in modification.changed_methods],
        "nloc": modification.nloc,
        "complexity": modification.complexity,
        "token_count": modification.token_count,
    }


def extract_branch_info(branch):
    return {
        "name": branch.name,
        "commit": {
            "sha": branch.commit.sha,
            "url": branch.commit.url
        },
    }


def extract_issue_info(issue):
    return {
        "number": issue.number,
        "title": issue.title,
        "body": issue.body,
        "state": issue.state,
        "creator": issue.user.login,
        "created_at": issue.created_at.isoformat(),
        "updated_at": issue.updated_at.isoformat(),
        "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
        "labels": [label.name for label in issue.labels],
        "assignees": [assignee.login for assignee in issue.assignees],
        "no_comments": issue.comments,
        "comments": [comment.body for comment in issue.get_comments()],
    }


def form_metadata(repository_url):
    token = ["YOUR_GITHUB_TOKEN_HERE"]  # replace these with your actual tokens
    github = Github(token)
    repo_name = extract_repo_name_from_url(repository_url)
    repo = github.get_repo(repo_name)

    def rate_limit_check(github):
        rate_limit = github.get_rate_limit().core
        if rate_limit.remaining < 10:  # adjust this number based on your needs
            reset_time = rate_limit.reset
            sleep_duration = (reset_time - datetime.utcnow()).total_seconds()
            print(f"Token rate limit hit, sleeping for {sleep_duration} seconds")
            time.sleep(max(0, sleep_duration))

    rate_limit_check(github)  # Check right after getting repo to ensure we have enough requests left

    repository_data = extract_repository_info(repo)
    repository_data["total_commits"] = repo.get_commits().totalCount
    repository_data["total_issues"] = repo.get_issues(state="all").totalCount
    repository_data["total_forks"] = repo.forks_count
    repository_data["total_stars"] = repo.stargazers_count
    repository_data["commits_on_date"] = {}
    repository_data["issues_on_date"] = {}

    # Extract commit and modification info
    for commit in Repository(repository_url).traverse_commits():
        commit_info = extract_commit_info(commit)

        date = commit_info["author"]["date"].split("T")[0]
        if date not in repository_data["commits_on_date"]:
            repository_data["commits_on_date"][date] = {
                "total_commits_on_day": 0,
                "commits": []
            }
        repository_data["commits_on_date"][date]["commits"].append(commit_info)
        repository_data["commits_on_date"][date]["total_commits_on_day"] += 1

        for modified_file in commit.modified_files:
            mod_info = extract_modification_info(modified_file)
            commit_info["modified_files"].append(mod_info)

    # Extract issue info
    issues = repo.get_issues(state="all")
    for issue in issues:
        issue_info = extract_issue_info(issue)

        date = issue_info["created_at"].split("T")[0]
        if date not in repository_data["issues_on_date"]:
            repository_data["issues_on_date"][date] = {
                "total_issues_on_day": 0,
                "issues": []
            }
        repository_data["issues_on_date"][date]["issues"].append(issue_info)
        repository_data["issues_on_date"][date]["total_issues_on_day"] += 1

        rate_limit_check(github)  # Check after each issue to ensure we don't hit the rate limit

    repository_data["created_at"] = datetime.utcnow().isoformat()
    repository_data["updated_at"] = datetime.utcnow().isoformat()

    return repository_data



async def clone_github_repo(repo_url, local_path="data_1"):
    # Extract repo name
    repo_name = repo_url.split("/")[-1].replace(".git", "")

    # Check if directory exists (i.e., repo is already cloned)
    if not os.path.isdir(os.path.join(local_path, repo_name)):
        try:
            process = await asyncio.create_subprocess_exec(
                "git", "clone", repo_url,
                cwd=local_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()

            meta_data = form_metadata(repo_url)
            with open(local_path + "/" + repo_name + "/repository_data.txt", "w", encoding='utf-8') as outfile:
                json.dump(meta_data, outfile, indent=1, default=handle_commit)

            find_and_convert_in_dir(local_path + "/" + repo_name)
        except Exception as e:
            return {"status": "error", "message": f"Exception occurred: {str(e)}"}

        if process.returncode == 0:
            return {"status": "success", "message": f"Cloned repo {repo_url}"}
        else:
            return {"status": "error", "message": f"Failed to clone repo {repo_url}", "detail": stderr.decode()}
    else:
        # try:
        #     meta_data = form_metadata(repo_url)
        #     with open(local_path + "/" + repo_name + "/repository_data.txt", "w", encoding='utf-8') as outfile:
        #         json.dump(meta_data, outfile, indent=1, default=handle_commit)
        #
        #     find_and_convert_in_dir(local_path + "/" + repo_name)
        #     return {"status": "success", "message": f"Metadata retrieved for {repo_url}"}
        # except Exception as e:
        #     return {"status": "error", "message": f"Exception occurred getting metadata: {str(e)}"}

        return {"status": "info", "message": f"Repo {repo_name} already exists locally"}
