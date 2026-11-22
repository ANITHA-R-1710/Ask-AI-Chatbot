
import streamlit as st
from chatbot import StudentChatbot
from gtts import gTTS
from io import BytesIO


# PAGE CONFIGURATION
st.set_page_config(
    page_title="Ask AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# CUSTOM CSS
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #172554);
    color: #ffffff;
}

header {
    background-color: transparent !important;
}

h1, h2, h3, h4, p, label {
    color: #ffffff !important;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #cbd5e1 !important;
    font-size: 17px;
    margin-bottom: 30px;
}

/* CHAT MESSAGES */
[data-testid="stChatMessage"] {
    background-color: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 12px;
}

/* CHAT INPUT */
[data-testid="stChatInput"] {
    background-color: #1e293b !important;
    border: 2px solid #60a5fa !important;
    border-radius: 14px !important;
}

[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    caret-color: #ffffff !important;
    background-color: #1e293b !important;
    font-size: 16px !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #cbd5e1 !important;
    -webkit-text-fill-color: #cbd5e1 !important;
    opacity: 1 !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #38bdf8 !important;
    box-shadow: 0 0 8px rgba(56, 189, 248, 0.4) !important;
}

/* BUTTONS */
.stButton > button {
    width: 100%;
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

/* SIDEBAR BACKGROUND */
[data-testid="stSidebar"] {
    background-color: #111827 !important;
}

/* SIDEBAR LIST TEXT - BRIGHT WHITE */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] ul,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li p {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    opacity: 1 !important;
    line-height: 1.8 !important;
}

/* SIDEBAR BULLET POINTS */
[data-testid="stSidebar"] li::marker {
    color: #60a5fa !important;
}

/* SIDEBAR HEADINGS */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4 {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* SIDEBAR DESCRIPTION */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #ffffff !important;
}

/* DIVIDERS */
hr {
    border-color: #475569 !important;
}

</style>
""", unsafe_allow_html=True)


# LOAD CHATBOT
@st.cache_resource
def load_chatbot():
    return StudentChatbot()


try:
    bot = load_chatbot()

except Exception as error:
    st.error("Unable to load the chatbot.")
    st.exception(error)
    st.stop()


# SESSION STATE
if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! 👋 Welcome to Ask AI!\n\n"
                "Ask me questions about programming, "
                "technology, academics and other topics "
                "available in my FAQ knowledge base.\n\n"
                "I'll display the answer and can read it aloud for you!"
            )
        }
    ]


# TEXT TO SPEECH
def generate_voice(text):

    try:
        audio_buffer = BytesIO()

        tts = gTTS(
            text=text,
            lang="en"
        )

        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return audio_buffer.getvalue()

    except Exception as error:

        print("Voice generation error:", error)
        return None


# PROCESS USER QUESTION
def process_question(question):

    if not question or not question.strip():
        return

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.spinner("🤖 Ask AI is searching for your answer..."):

        response = bot.get_response(question)

        audio_data = generate_voice(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "audio": audio_data
    })


# SIDEBAR
with st.sidebar:

    st.title("🤖 Ask AI")

    st.write("Your FAQ-Based Learning Assistant")

    st.markdown("---")

    st.subheader("📚 What I Can Help With")

    st.write("""
    - Python Programming
    - Java Programming
    - C and C++
    - Artificial Intelligence
    - Machine Learning
    - Deep Learning
    - Data Science
    - Data Analytics
    - DBMS and SQL
    - Operating Systems
    - Computer Networks
    - Cybersecurity
    - Mathematics
    - Exam Preparation
    - Internship Guidance
    - Placement Preparation
    - English Communication
    """)

    st.markdown("---")

    st.subheader("🔊 Voice Assistant")

    st.write("""
    Ask your question using the text box.
    Ask AI will display the matching answer
    and provide audio playback.
    """)

    st.markdown("---")

    st.subheader("💡 About")

    st.write(
        "Ask AI is a FAQ-based chatbot built using "
        "Python, Streamlit and Natural Language Processing. "
        "It uses a predefined FAQ knowledge base "
        "and gTTS for voice responses."
    )

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Chat cleared! 😊 "
                    "What would you like to ask?"
                )
            }
        ]

        st.rerun()


# MAIN HEADER
st.markdown(
    '<div class="main-title">🤖 Ask AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask Anything. Learn Everything.</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# SUGGESTED QUESTIONS
st.subheader("✨ Try Asking")

suggestions = [
    "What is Python?",
    "What is Artificial Intelligence?",
    "Explain Machine Learning",
    "What is DBMS?",
    "How should I prepare for exams?"
]

columns = st.columns(5)

for index, question in enumerate(suggestions):

    if columns[index].button(
        question,
        key=f"suggestion_{index}"
    ):

        process_question(question)
        st.rerun()


st.markdown("---")


# DISPLAY CHAT HISTORY
st.subheader("💬 Chat Conversation")

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            if message.get("audio"):

                st.audio(
                    message["audio"],
                    format="audio/mp3"
                )

            elif "audio" in message:

                st.caption(
                    "🔊 Audio is currently unavailable."
                )


# TEXT INPUT
user_input = st.chat_input(
    "💬 Ask me anything..."
)

if user_input:

    process_question(user_input)
    st.rerun()


# FOOTER
st.markdown("---")

st.markdown(
    """
    <center>
    Made with ❤️ using Python, Streamlit,
    NLP and Voice Technology
    </center>
    """,
    unsafe_allow_html=True
)
