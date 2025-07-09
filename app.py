import asyncio
import platform

# ✅ Fix for Windows subprocess compatibility
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
from team import get_dsa_team
from autogen_agentchat.base import TaskResult  

# Streamlit app config
st.set_page_config(page_title="DSAlyzer", page_icon="🧠")
st.title("🧠 DSAlyzer - DSA Problem Solver")
st.markdown("📌 **Enter your DSA problem or question:**")

user_input = st.text_area("Write your question here 👇")

if st.button("Submit") and user_input.strip() != "":
    with st.spinner("Thinking... 🧠"):

        async def run_task(task):
            team = get_dsa_team()
            messages = []

            async for msg in team.run_stream(task=task):
                if hasattr(msg, "source") and hasattr(msg, "content"):
                    if msg.content is not None and str(msg.content).strip() != "undefined":
                        messages.append(f"{msg.source}: {msg.content}")
                elif isinstance(msg, TaskResult):
                    messages.append(f"✅ Task completed. Stop Reason: {msg.stop_reason}")
                else:
                    messages.append(f"⚠️ Unrecognized message: {msg}")

            return messages

        try:
            output = asyncio.run(run_task(user_input))
            for msg in output:
                if msg and str(msg).strip().lower() != "undefined":
                    st.markdown(f"```\n{msg}\n```")
        except Exception as e:
            st.error(f"❌ Error occurred:\n\n{e}")
