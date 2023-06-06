from langchain.tools import StructuredTool

TOOLS = [
    StructuredTool.from_function(
        func=lambda x: "test_repo", name="get_repo_name", description="Returns the name of the current repository."
    ),
    StructuredTool.from_function(
        func=lambda x: "test_branch", name="get_branch_name", description="Returns the name of the current branch."
    ),
    StructuredTool.from_function(
        func=lambda x: "test_remote", name="get_remote_name", description="Returns the name of the current remote."
    ),
    StructuredTool.from_function(
        func=lambda x: "test_remote_url", name="get_remote_url",
        description="Returns the remote URL of the current repository."
    ),
    StructuredTool.from_function(
        func=lambda x: "test_current_path", name="get_current_path", description="Returns current path."
    ),
    StructuredTool.from_function(
        func=lambda x: "test_current_commit", name="get_commit_name", description="Returns current commit."
    ),
    StructuredTool.from_function(
        func=lambda x: "[changed_file1, changed_file2, changed_file3]", name="get_list_of_changed_files",
        description="Returns the changes in the current repository."
    ),
    StructuredTool.from_function(
        func=lambda x: "[available_file1, available_file2, available_file3]", name="get_list_of_available_files",
        description="Returns the list of available files in the current repository."
    ),
    StructuredTool.from_function(
        func=lambda x: "test_user", name="get_current_user", description="Returns the current user."
    )
]
