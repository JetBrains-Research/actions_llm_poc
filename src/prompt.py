from langchain import PromptTemplate, FewShotPromptTemplate
from langchain.prompts.chat import (
    SystemMessagePromptTemplate, HumanMessagePromptTemplate, BaseChatPromptTemplate,
)

from git_actions import GitActions
from tools import TOOLS

EXAMPLES = [
    {
        'question': 'i want to change remote',
        'answer': f"""
Thought: I know the final answer
Final_Answer:
{GitActions.MANAGE_REMOTES.format()}
        """

    },
    {
        'question': 'create repo actions_llm_poc',
        'answer': f"""
Thought: I know the final answer
Final_Answer:
{GitActions.CREATE_REPO.format(Path='./actions_llm_poc')}
        """

    },
    {
        'question': 'create branch test',
        'answer': f"""
Thought: I need to know current commit from which to create a branch
Action: get_commit_name
Observation: test_current_commit
Thought: I know the final answer
Final_Answer: 
{GitActions.NEW_BRANCH.format(Name='test', Commit='test_current_commit', isCheckout='True')}
        """
    },
    {
        'question': 'clone GitHub repo great_prj',
        'answer': f"""
Thought: I need to know current user
Action: get_current_user
Observation: test_user
Thought: I know the final answer
Final_Answer: 
{
        GitActions.CLONE.format(Path='https://github.com/test_user/great_prj', Directory='./great_prj')
        }
        """
    },
    {
        'question': 'add remote origin',
        'answer': f"""
Thought: I know the final answer
Final_Answer:
{GitActions.ADD_REMOTE.format(Name='origin', URL='?')}
        """

    },
    {
        'question': 'push changes with message "Fix-243"',
        'answer': f"""
Thought: I need to know what changes have been made
Action: get_list_of_changed_files
Observation: [changed_file1, changed_file2, changed_file3]
Thought: I need to know current remote
Action: get_remote_name
Observation: test_remote
Thought: I need to know current branch
Action: get_branch_name
Observation: test_branch
Final_Answer:
{GitActions.COMMIT.format(Files='[changed_file1, changed_file2, changed_file3]', Message='Fix-243')}
{GitActions.PUSH.format(Remote='test_remote', Branch='test_branch')}
        """

    },
    {
        'question': 'what has been changed in file1?',
        'answer': f"""
Thought: I know the final answer
Final_Answer:
{GitActions.SHOW_DIFF.format(Item='file1')}
        """

    },
]


class ActionsPromptTemplate(BaseChatPromptTemplate):
    general_instructions_template = """
You are an Interactive Development Environment (IDE) agent.
Your goal is to translate a user's request into a series of actions that can be executed by the IDE.

You MUST use actions ONLY from the list:
{actions}

Each action is in the following format: <action's name>[<action's parameters>].

Your answer will be parsed AUTOMATICALLY by an IDE without user involvement.
Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final_Answer: the final answer to the original input question

Final Answer MUST BE in the following format:
Action1[Parameter1, Parameter2] 
Action2
Action3[?] 
...
When you don't know what is the correct parameter for an action, use '?'.
When you are not sure what to answer, use UNKNOWN.

You have access to the following tools:

{tools}
    """
    examples_template = FewShotPromptTemplate(
        examples=EXAMPLES,
        example_prompt=PromptTemplate(input_variables=["question", "answer"], template="Question: {question} {answer}"),
        suffix="",
        input_variables=[]
    ).format()
    human_template = """
Begin!

Question: {input}
{agent_scratchpad}
    """
    tools_prompt = "\n".join([f"{tool.name}: {tool.description}" for tool in TOOLS])
    tool_names = [tool.name for tool in TOOLS]
    actions = GitActions.all_actions()

    def format_messages(self, **kwargs):
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        kwargs["agent_scratchpad"] = thoughts

        system_kwargs = {"actions": self.actions, "tools": self.tools_prompt, "tool_names": self.tool_names}
        system_prompt = '\n \n'.join([self.general_instructions_template, self.examples_template])
        system_message = SystemMessagePromptTemplate.from_template(system_prompt).format(**system_kwargs)

        # return [HumanMessage(content=formatted)]
        human_message = HumanMessagePromptTemplate.from_template(self.human_template).format(**kwargs)
        return [system_message, human_message]
