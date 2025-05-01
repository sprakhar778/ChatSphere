import streamlit as st
import uuid
import datetime
from graph import workflow
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages.tool import ToolMessage
import base64
from io import BytesIO



def load_image_as_base64(image_path):
    """
    Load an image from a file path and encode it as a base64 string.

    Args:
        image_path (str): The file path of the image.

    Returns:
        str: Base64 encoded string of the image.
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
# Page configuration
st.set_page_config(
    page_title="LangGraph AI",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Streamlit app background and font */
    .reportview-container {
        background-color: #f0f2f6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Chat container styling */
    .stChatMessage>div {
        border-radius: 16px;
        padding: 8px 16px;
        margin-bottom: 8px;
    }
    /* User message bubble */
    .stChatMessage_user>div {
        background-color: #ffffff;
        color: #000000;
        align-self: flex-end;
    }
    /* Assistant message bubble */
    .stChatMessage_assistant>div {
        background-color: #0078d4;
        color: #ffffff;
        align-self: flex-start;
    }
    /* Title styling */
    .main .block-container h1 {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0078d4;
        margin-bottom: 0.5rem;
    }
    /* Sidebar chat history styles */
    .chat-history-item {
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 8px;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .chat-history-item:hover {
        background-color: rgba(0, 120, 212, 0.1);
    }
    .chat-history-item.active {
        background-color: rgba(0, 120, 212, 0.2);
        font-weight: bold;
    }
    /* Chat meta info */
    .chat-meta {
        font-size: 0.8rem;
        color: #666;
        margin-top: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# Define the system prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a helpful, concise, and intelligent AI assistant. "
        "You have access to a **Tavily search tool** which provides web results. "
        "Use this tool **only when the user asks about recent, factual, or specific information** "
        "that you are not confident about or that may have changed (e.g., current events, news, live data, etc).\n\n"
        "If the user's question is general, conversational, or something you already know with high certainty, "
        "**respond directly without calling the tool**.\n\n"
        "When using the tool, take its output as context and clearly present the final answer after reviewing the result"
    )),
    ("human", "{input}")
])

# Initialize session state variables
if "chats" not in st.session_state:
    # Store multiple chats with their histories
    # Format: {chat_id: {"title": title, "history": [(role, content)], "created_at": timestamp}}
    st.session_state.chats = {}

if "current_chat_id" not in st.session_state:
    # Create initial chat
    new_chat_id = str(uuid.uuid4())
    st.session_state.chats[new_chat_id] = {
        "title": "New Chat",
        "history": [],
        "created_at": datetime.datetime.now()
    }
    st.session_state.current_chat_id = new_chat_id

if "pending_user_input" not in st.session_state:
    st.session_state.pending_user_input = None

# Function to create a new chat
def new_chat():
    new_chat_id = str(uuid.uuid4())
    st.session_state.chats[new_chat_id] = {
        "title": "New Chat",
        "history": [],
        "created_at": datetime.datetime.now()
    }
    st.session_state.current_chat_id = new_chat_id

# Function to switch to a different chat
def switch_chat(chat_id):
    st.session_state.current_chat_id = chat_id

# Function to delete a chat
def delete_chat(chat_id):
    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]
        # If we deleted the current chat, switch to another one or create a new one
        if chat_id == st.session_state.current_chat_id:
            if st.session_state.chats:
                st.session_state.current_chat_id = next(iter(st.session_state.chats))
            else:
                new_chat()

# Function to update chat title based on first message
def update_chat_title(chat_id, user_input):
    current_title = st.session_state.chats[chat_id]["title"]
    if current_title == "New Chat" and user_input:
        # Use the first ~30 chars of user input as the chat title
        new_title = user_input[:30] + ("..." if len(user_input) > 30 else "")
        st.session_state.chats[chat_id]["title"] = new_title

# Function to export chat history
def export_chat():
    chat_history = st.session_state.chats[st.session_state.current_chat_id]["history"]
    chat_export = ""
    for role, content in chat_history:
        chat_export += f"{role.upper()}: {content}\n\n"
    return chat_export

# Sidebar with chat history
with st.sidebar:
    st.title("Chat History")
    
    # New chat button at the top
    if st.button("+ New Chat", key="new_chat_button"):
        new_chat()
        st.rerun()
    
    st.markdown("---")
    
    # Display all chats in sidebar
    if st.session_state.chats:
        for chat_id, chat_data in sorted(
            st.session_state.chats.items(),
            key=lambda x: x[1]["created_at"],
            reverse=True
        ):
            col1, col2 = st.columns([0.8, 0.2])
            
            with col1:
                # Format timestamp to just show date if not today
                created_date = chat_data["created_at"].strftime("%b %d") if chat_data["created_at"].date() != datetime.datetime.now().date() else chat_data["created_at"].strftime("%H:%M")
                
                # Chat entry that can be clicked
                if st.button(
                    f"{chat_data['title']}",
                    key=f"chat_{chat_id}",
                    use_container_width=True,
                    type="secondary" if chat_id != st.session_state.current_chat_id else "primary"
                ):
                    switch_chat(chat_id)
                    st.rerun()
            
            with col2:
                if chat_id != st.session_state.current_chat_id:
                    if st.button("🗑️", key=f"delete_{chat_id}", help="Delete this chat"):
                        delete_chat(chat_id)
                        st.rerun()
    
    st.markdown("---")
    
    # Chat Settings
    with st.expander("Settings"):
        if st.button("Export Current Chat"):
            chat_export = export_chat()
            st.download_button(
                label="Download Chat",
                data=chat_export,
                file_name=f"chat_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    st.markdown("---")
    st.write("**About**")
    st.write("AI Assistant built with LangGraph.")

# No theme or font size adjustments needed

# Title display
# ------------------------------ Title & Subtitle ------------------------------

# Display Hero Image
logo_base64 = load_image_as_base64("logo.png")

st.markdown(    f"""
    <style>
    .hero-section {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-top: 40px;
    }}
    .logo-image {{
        width: 500px;
        height: 380px;
       
        
    }}
   
   
    </style>

    <div class="hero-section">
        <img src="data:image/png;base64,{logo_base64}" class="logo-image" alt="Synthesia Logo">
       
       
    </div>
    """,
    unsafe_allow_html=True
)


# Get current chat history
current_chat = st.session_state.chats[st.session_state.current_chat_id]
chat_history = current_chat["history"]

# Display current chat history
for role, content in chat_history:
    with st.chat_message(role):
        st.markdown(content)

# Chat input
user_input = st.chat_input("Ask me anything...")

# Process new user input
if user_input:
    st.session_state.pending_user_input = user_input

if st.session_state.pending_user_input:
    user_input = st.session_state.pending_user_input
    
    # Update chat title if this is the first message
    update_chat_title(st.session_state.current_chat_id, user_input)
    
    # Add message to history
    chat_history.append(("user", user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    formatted_messages = prompt.format_messages(input=user_input)
    config = {"configurable": {"thread_id": st.session_state.current_chat_id}}

    # Show typing indicator
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        with st.spinner("Assistant is typing…"):
            for event in workflow.stream(
                {"messages": formatted_messages},
                config,
                stream_mode="values"
            ):
                msg = event["messages"][-1]
                
                if isinstance(msg, ToolMessage):
                    # Optionally show tool usage message
                    response_container.markdown("_Searching for information..._")
                    continue
                chunk = msg.content
                full_response = chunk
                print("*****8888888",chunk)
                response_container.markdown(full_response)

        chat_history.append(("assistant", full_response))

    # Clear pending input
    st.session_state.pending_user_input = None
    
    # Force a rerun to update the sidebar with new chat title
    st.rerun()