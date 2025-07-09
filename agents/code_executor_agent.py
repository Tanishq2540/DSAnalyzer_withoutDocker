from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor


class SafeCodeExecutor(LocalCommandLineCodeExecutor):
    async def execute_code_blocks(self, code_blocks, **kwargs):
        wrapped_blocks = []
        for block in code_blocks:
            if isinstance(block, str) and "```" not in block:
                block = f"```python\n{block.strip()}\n```"
            wrapped_blocks.append(block)
        return await super().execute_code_blocks(wrapped_blocks, **kwargs)

def get_code_executor_agent():
    executor = SafeCodeExecutor()  

    code_executor_agent = CodeExecutorAgent(
        name='CodeExecutorAgent',
        code_executor=executor
    )

    return code_executor_agent, executor
