###
# For the simplicity we will not execute the proposed actions. We only aim for the correct sequence of actions.
from enum import Enum


class GitActions(Enum):
    # Git repo actions
    CLONE = 'Clone[Path, Directory]', 'clone repository from Path to Directory'
    CREATE_REPO = 'CreateRepository[Path]', 'create repository at Path'
    MANAGE_REMOTES = 'ManageRemotes', 'open tool window for managing remotes'
    ADD_REMOTE = 'AddRemote[Name, URL]', ' add remote with Name and URL'
    REMOVE_REMOTE = 'RemoveRemote[Name]', ' remove remote with Name'
    NEW_BRANCH = 'NewBranch[Name, Commit, isCheckout]', \
        ' create new branch with Name from commit Commit and checkout if isCheckout'
    REMOVE_BRANCH = 'RemoveBranch[Name]', ' remove branch with Name', 'RemoveBranch'
    NEW_TAG = 'NewTag[Name, Commit]', ' create new tag with Name from commit Commit'

    # Git changes actions
    PULL = 'Pull[Remote, Branch]', ' pull changes from Remote to Branch'
    FETCH = 'Fetch[Remote, Branch]', ' fetch changes from Remote to Branch'
    ADD = 'Add[Files]', ' add Files to the staging area'
    COMMIT = 'Commit[Files, Message, isAmend]', ' commit Files with Message and amend if isAmend'
    PUSH = 'Push[Remote, Branch]', ' push changes from Remote to Branch'
    ROLLBACK = 'Rollback[Files]', ' rollback changes in Files'

    # Git commits actions
    REVERT = 'Revert[Commit]', ' revert Commit'
    CHERRY_PICK = 'CherryPick[Commit]', ' cherry pick Commit'

    # Git info actions
    SHOW_HISTORY = 'ShowHistory[Item]', ' show history of Item'
    SHOW_DIFF = 'ShowDiff[Item]', ' show diff of Item'
    COMPARE_WITH_BRANCH = 'CompareWithBranch[Item, Branch]', \
        ' compare current version of Item with it\'s version in Branch'
    SHOW_REPOSITORY_AT_REVISION = 'ShowRepositoryAtRevision[Commit]', ' show repository at Commit'

    @staticmethod
    def all_actions():
        return '\n'.join([' - '.join([action.value[0], action.value[1]]) for action in GitActions])

    def format(self, **kwargs):
        formatted_value = self.value[0]
        for key, value in kwargs.items():
            formatted_value = formatted_value.replace(key, value)
        return formatted_value
