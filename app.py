import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if you're using it)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Ensure you have set OPENAI_API_KEY in your environment variables
client = OpenAI(api_key=api_key)

# Define the character template with custom instructions for structured and complete responses
gandhi_template = {
    "name": "Mahatma Gandhi",
    "personality": (
        "I am Mahatma Gandhi, a peaceful leader who believes in non-violence (Ahimsa), truth (Satya), and unity. "
        "I advocate for social justice and equality, and I always encourage peaceful ways of resolving conflicts."
    ),
    "speaking_style": (
        "I speak calmly, using metaphors and spiritual references where needed. "
        "I blend English and Hindi (Hinglish) to connect, keeping responses short and simple, and avoiding harmful or inappropriate topics."
    ),
    "tone": "Respectful, wise, and focused on peaceful solutions.",
    "response_instructions": (
        "Please ensure that responses are well-structured, concise, and complete within 2-3 sentences. "
        "Responses should avoid abrupt endings, ensuring the message is fully conveyed in a clear and respectful manner."
    ),
    "non_responding_topics": ["violence", "harmful behavior", "inappropriate or offensive questions"],
}

# Function to handle custom questions like "Who built this chatbot?"
def custom_responses(prompt):
    if "who built this chatbot" in prompt.lower() or "who created this chatbot" in prompt.lower():
        return "This chatbot was created by Build Fast with AI."
    return None

# Function to generate GPT-4 responses
def get_gpt4_response(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=120,  # Limit token count to encourage concise responses
            temperature=0.5,  # Keep balanced creativity
            top_p=1,  # Focus on coherent responses
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "I apologize, I cannot respond at the moment."

# Streamlit app title
st.title(f"Chat with {gandhi_template['name']}")

# Initialize chat history if not present
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": f"You are {gandhi_template['name']}. "
                       f"Your personality: {gandhi_template['personality']}. "
                       f"Your speaking style: {gandhi_template['speaking_style']}. "
                       f"Tone: {gandhi_template['tone']}. "
                       f"{gandhi_template['response_instructions']}. "
                       f"Do not respond to questions related to: {', '.join(gandhi_template['non_responding_topics'])}."
        }
    ]

# Display previous chat messages (except system messages)
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask Mahatma Gandhi anything."):
    # Display the user's message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check if the prompt is asking about who built the chatbot
    custom_response = custom_responses(prompt)
    if custom_response:
        response = custom_response
    else:
        # Get GPT-4 response if no custom response is triggered
        response = get_gpt4_response(st.session_state.messages)

    # Display the response and update chat history
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
