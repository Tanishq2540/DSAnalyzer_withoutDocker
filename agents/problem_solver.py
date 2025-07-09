from autogen_agentchat.agents import AssistantAgent
from config.settings import get_model_client


model_client = get_model_client()

def get_problem_solver_agent():
    """
    Function to get the problem solver agent.
    This agent is responsible for solving DSA problems.
    It will work with the code executor agent to execute the code.
    """
    problem_solver_agent = AssistantAgent(
            name="DSA_Problem_Solver_Agent",
            description="An agent that solves DSA problems",
            model_client=model_client,
            system_message="""
                You are a problem solver agent that is an expert in solving DSA problems.
                You will be working with code executor agent to execute code.
                You will be given a coding task and you should return a python code solving that problem.
                If the task is not related to coding, respond only with "Kindly ask a coding related problem", after this mention "STOP" to end the execution. 
                At the beginning of your response you have to specify your plan to solve the task.
                Then you should give the code in a code block.(Python)
                You should write code in a one code block at a time and then pass it to code executor agent to execute it.
                Make sure that we have atleast 3 test cases for the code you write.
                Send the code along with the test cases written to the code executor agent to verify the correctness of the code.
                Once the code is executed, you have the results.
                You should explain the results in detail before outputting the final code.
                In the end, you have to say "STOP" to stop the conversation.

                """
        )


    
    return problem_solver_agent