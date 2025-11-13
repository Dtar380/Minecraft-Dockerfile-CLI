#################################################
# IMPORTING MODULES
#################################################
from __future__ import annotations

import os
import random
from typing import Any

import requests  # type: ignore

#################################################
# CODE
#################################################
#####  GLOBAL VARIABLES
API = "https://api.github.com/"

API_TOKEN = os.environ["API_KEY"]
REPO = os.environ["REPO"]

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer " + API_TOKEN,
    "X-GitHub-Api-Version": "2022-11-28",
}


#####  FUNCTIONS
## Actions to perform
def get_issue() -> int:
    response = requests.get(f"{API}repos/{REPO}/issues", headers=headers).json()
    return response[0]["number"]  # type: ignore


def close_issue(issue_number: int) -> None:
    payload = '{"state": "closed"}'
    requests.patch(
        f"{API}repos/{REPO}/issues/{issue_number}",
        data=payload,
        headers=headers,
    )


def comment_issue(issue_number: int, comment: str) -> None:
    payload = f'{{"body": "{comment}"}}'
    requests.post(
        f"{API}repos/{REPO}/issues/{issue_number}/comments",
        data=payload,
        headers=headers,
    )


def add_assignees(issue_number: int, assignees: str) -> None:
    assignees_str = "["

    for i, assignee in enumerate(assignees):
        if i != 0:
            assignees_str += ","
        assignees_str += f'"{assignee}"'

    assignees_str += "]"

    payload = f'{{"assignees":{assignees_str}}}'
    requests.post(
        f"{API}repos/{REPO}/issues/{issue_number}/assignees",
        data=payload,
        headers=headers,
    )


## Verifications to perform
# TEMPLATES
def check_if_follows_template(issue_number: int) -> bool:
    issue = requests.get(
        f"{API}repos/{REPO}/issues/{issue_number}", headers=headers
    ).json()
    if not issue["labels"] and not issue["body"]:
        return False
    return True


# ASSIGNEES
def check_for_assignable_users(issue_number: int) -> str:
    contributors = check_for_colaborators()

    assignees = []
    for contributor in contributors:
        if (
            requests.get(
                f"{API}repos/{REPO}/issues/{issue_number}/assignees/{contributor}"
            ).status_code
            == 204
        ):
            assignees.append(contributor)

    if len(assignees) < 3:
        return assignees  # type: ignore

    return random.sample(assignees, 3)  # type: ignore


def check_for_colaborators() -> list[Any]:
    response = requests.get(
        f"{API}repos/{REPO}/contributors", headers=headers
    ).json()

    colaborators = []
    for colaborator in response:
        colaborators.append(colaborator["login"])

    return colaborators


## MAIN ENTRY POINT
def main() -> None:
    issue_number = get_issue()
    if not check_if_follows_template(issue_number):
        comment = "This Issue is getting closed because it does not follow any given template.<br>\
Try reposting the issue following one of the given templates."
        comment_issue(issue_number, comment)
        close_issue(issue_number)

    elif check_for_assignable_users(issue_number):
        assignees = check_for_assignable_users(issue_number)
        comment = "Thanks for submitting your issue. An assignee will be with you very soon."
        comment_issue(issue_number, comment)
        add_assignees(issue_number, assignees)

    else:
        comment = "Thanks for submitting your issue. Unfortunately we could not find an aviable assignee for you.<br>\
Wait until an assignee is aviable and comes to help you."
        comment_issue(comment)  # type: ignore


#####  RUN FILE
if __name__ == "__main__":
    main()
