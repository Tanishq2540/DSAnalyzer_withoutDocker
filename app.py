import streamlit as st
from team import get_dsa_team_and_docker
from config.docker_utils import start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
import asyncio

st.set_page_config(page_title="DSAlyzer", layout="centered")

st.title("🧠 DSAlyzer - DSA Problem Solver")
st.write("Welcome to AlgoGenie, your personal DSA problem solver! Ask any Data Structures and Algorithms (DSA) question below:")

# Initialize session state
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "task_running" not in st.session_state:
    st.session_state.task_running = False

task = st.text_input("📌 Enter your DSA problem or question:", value='Write a function to add two numbers')

# Async DSA run
async def run(team, docker, task):
    try:
        await start_docker_container(docker)
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                msg = f"{message.source} : {message.content}"
                st.session_state.chat_log.append(msg)
                yield msg
            elif isinstance(message, TaskResult):
                msg = f"Stop Reason: {message.stop_reason}"
                st.session_state.chat_log.append(msg)
                yield msg
    except Exception as e:
        err = f"Error: {e}"
        st.session_state.chat_log.append(err)
        yield err
    finally:
        await stop_docker_container(docker)


if st.button("🚀 Run"):
    st.session_state.chat_log = []
    st.session_state.task_running = True
    team, docker = get_dsa_team_and_docker()

    async def collect_messages():
        async for msg in run(team, docker, task):
            if isinstance(msg, str):
                if msg.startswith("user"):
                    with st.chat_message('user', avatar='👤'):
                        st.markdown(msg)
                elif msg.startswith('DSA_Problem_Solver_Agent'):
                    with st.chat_message('assistant', avatar='🧑‍💻'):
                        st.markdown(msg)
                elif msg.startswith('CodeExecutorAgent'):
                    with st.chat_message('assistant', avatar='🤖'):
                        st.markdown(msg)
                elif msg.startswith('Stop Reason:'):
                    with st.chat_message('stopper', avatar='🚫'):
                        st.markdown(msg)

    asyncio.run(collect_messages())

for msg in st.session_state.chat_log:
    if msg.startswith("user"):
        with st.chat_message('user', avatar='👤'):
            st.markdown(msg)
    elif msg.startswith('DSA_Problem_Solver_Agent'):
        with st.chat_message('assistant', avatar='🧑‍💻'):
            st.markdown(msg)
    elif msg.startswith('CodeExecutorAgent'):
        with st.chat_message('assistant', avatar='🤖'):
            st.markdown(msg)
    elif msg.startswith('Stop Reason:'):
        with st.chat_message('stopper', avatar='🚫'):
            st.markdown(msg)

st.markdown("---")
if st.button("🔁 Reset", key="reset_btn"):
    st.session_state.chat_log = []
    st.session_state.task_running = False
    st.rerun()
