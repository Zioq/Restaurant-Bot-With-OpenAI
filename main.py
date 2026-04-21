""" 

uv run streamlit run main.py
 """


import dotenv
dotenv.load_dotenv()
from openai import OpenAI
import asyncio
import streamlit as st
from agents import (
    Runner,
    SQLiteSession,
    function_tool, 
    RunContextWrapper,
    InputGuardrailTripwireTriggered
)

from models import CustomerAccountContext
from my_agents.triage_agent import triage_agent

client = OpenAI()

if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "restaurant-chat-history",
        "restaurant-support-memory.db"
    )
session = st.session_state["session"]

if "agent" not in st.session_state:
    st.session_state["agent"] = triage_agent

customer_account_ctx = CustomerAccountContext(
    customer_id= "customer_ss10",
    name = "Robert Han"
)

async def paint_history():
    messages = await session.get_items()
    for message in messages:
        if "role" in message:
            with st.chat_message(message["role"]):
                if message["role"] == "user":
                    st.write(message["content"])
                else:
                    if message["type"] == "message":
                        st.write(message["content"][0]["text"])


asyncio.run(paint_history())

async def run_agent(message):
    with st.chat_message("ai"):
        text_placeholder = st.empty()
        response = ""

        st.session_state["text_placeholder"] = text_placeholder

        try:
            stream = Runner.run_streamed(
                st.session_state["agent"],
                message,
                session=session,
                context=customer_account_ctx,
            )

            async for event in stream.stream_events():
                if event.type == "raw_response_event":
                    if event.data.type == "response.output_text.delta":
                        response += event.data.delta
                        text_placeholder.write(response)

                elif event.type == "agent_updated_stream_event":
                    if st.session_state["agent"].name != event.new_agent.name:
                        st.write(
                            f"🤖 Transferred from "
                            f"{st.session_state['agent'].name} "
                            f"to {event.new_agent.name}"
                        )
                        st.session_state["agent"] = event.new_agent
                        text_placeholder = st.empty()
                        response = ""

        
        except InputGuardrailTripwireTriggered:
            text_placeholder.write("I cannot help with this request.")


message = st.chat_input("Please write a message for your assistant for our restaurant. Thank you for choosing us.")

if message:
    if "text_placeholder" in st.session_state:
        st.session_state["text_placeholder"].empty()

    with st.chat_message("human"):
        st.write(message)
    asyncio.run(run_agent(message))

with st.sidebar:
    reset = st.button("Reset memory")
    if reset:
        asyncio.run(session.clear_session())
    st.write(asyncio.run(session.get_items()))