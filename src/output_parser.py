import re
from typing import Union

from langchain.agents import AgentOutputParser
from langchain.schema import AgentAction, AgentFinish


class ActionsOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if agent should finish
        if "Final_Answer:" in llm_output:
            actions_to_perform = re.search(r"Final_Answer:[\s]*(.*)", llm_output, re.DOTALL).group(1)
            parsed_actions = self.parse_actions_with_parameters(actions_to_perform)
            output = ""
            for action_name, parameters in parsed_actions:
                ide_action = ActionsOutputParser.get_ide_action(action_name, parameters)
                output += f'{ide_action} \n'

            return AgentFinish(return_values={"output": output}, log=llm_output)
        # Parse out the tool_action and tool_action input
        match = re.search(r"Action:[\s]*(.*)", llm_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        tool_action = match.group(1).strip()
        # Return the tool_action and tool_action input
        return AgentAction(tool=tool_action, tool_input="", log=llm_output)

    def parse_actions_with_parameters(self, llm_output: str):

        # Split output to the series of actions
        actions = llm_output.split("\n")
        parsed_actions = []

        for i in range(len(actions)):
            action = actions[i]
            match = re.match(r"(\w+)\[(.+)\]", action)
            if match:
                action_name = match.group(1)
                parameters = [param.strip() for param in match.group(2).split(',')]
                parsed_actions.append((action_name, parameters))
            else:
                raise ValueError(f"Could not parse action: `{action}`")
        return parsed_actions

    @staticmethod
    def get_ide_action(action_name: str, action_parameters: list) -> str:
        # This function imitates actions performing by IDE.
        # It takes the name of actions and outputs description of it like if it is actually performed.
        # In real life, this function should be replaced by real IDE's actions.
        if action_name == 'Clone':
            return f'Cloning repository from {action_parameters[0]} to {action_parameters[1]}'
        elif action_name == 'CreateRepository':
            return f'Creating reposit ory from {action_parameters[0]}'
        elif action_name == 'ManageRemotes':
            return f'Open \'Manage Remotes\' window'
        elif action_name == 'AddRemote':
            return f'Adding remote {action_parameters[0]} from {action_parameters[1]}'
        elif action_name == 'RemoveRemote':
            return f'Removing remote {action_parameters[0]}'
        elif action_name == 'NewBranch':
            return f'Creating new branch {action_parameters[0]} from commit {action_parameters[1]}'
        elif action_name == 'NewTag':
            return f'Creating new tag {action_parameters[0]} from commit {action_parameters[1]}'
        elif action_name == 'Pull':
            return f'Pulling from {action_parameters[0]}'
        elif action_name == 'Fetch':
            return f'Fetching from {action_parameters[0]} / {action_parameters[1]}'
        elif action_name == 'Add':
            return f'Adding {action_parameters[0]}'
        elif action_name == 'Commit':
            return f'Committing {action_parameters[0]} with message {action_parameters[1]}, isCheckout={action_parameters[2]}'
        elif action_name == 'Push':
            return f'Pushing to {action_parameters[0]} / {action_parameters[1]}'
        elif action_name == 'Rollback':
            return f'Rollback {action_parameters[0]}'
        elif action_name == 'Revert':
            return f'Reverting {action_parameters[0]}'
        elif action_name == 'CherryPick':
            return f'Cherry-picking {action_parameters[0]}'
        elif action_name == 'ShowHistory':
            return f'Showing history of {action_parameters[0]}'
        elif action_name == 'ShowDiff':
            return f'Showing diff of {action_parameters[0]}'
        elif action_name == 'CompareWithBranch':
            return f'Comparing {action_parameters[0]} with version in branch {action_parameters[1]}'
        elif action_name == 'ShowRepositoryAtRevision':
            return f'Showing repository at revision {action_parameters[0]}'
        else:
            raise ValueError(f"Could not parse action: `{action_name}`")
