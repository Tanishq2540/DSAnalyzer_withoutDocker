from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

def get_code_executor_agent():
    executor = LocalCommandLineCodeExecutor()

    code_executor_agent = CodeExecutorAgent(
        name='CodeExecutorAgent',
        code_executor=executor
    )

    return code_executor_agent, executor

