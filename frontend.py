import streamlit as st
from ai_researcher import graph, INITIAL_PROMPT

st.set_page_config(
    page_title="ThesisCraft",
    page_icon="📄",
    layout="wide",
)

st.title("📄 ThesisCraft")
st.caption("AI Research Assistant powered by LangGraph + Ollama")

# ---------------- Session ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- Chat ---------------- #

prompt = st.chat_input("Enter a research topic...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()
        response_text = ""

        input_data = {
            "messages": [
                {
                    "role": "system",
                    "content": INITIAL_PROMPT,
                }
            ]
            + st.session_state.messages
        }

        for event in graph.stream(
            input_data,
            stream_mode="values",
        ):

            message = event["messages"][-1]

            # Tool Calls
            if getattr(message, "tool_calls", None):
                for tool in message.tool_calls:
                    st.info(f"🔧 Using tool: **{tool['name']}**")

            # Assistant Response
            if getattr(message, "content", None):

                if isinstance(message.content, str):
                    response_text = message.content

                elif isinstance(message.content, list):
                    response_text = "".join(
                        part.get("text", "")
                        for part in message.content
                        if isinstance(part, dict)
                    )

                placeholder.markdown(response_text)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response_text,
            }
        )