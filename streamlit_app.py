import streamlit as st
import replicate
import requests

# Set page config to include tab title
st.set_page_config(page_title="recraft-v3 generator")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# User ID input and session creation
st.title("Image generator")
checkbox_1 = st.checkbox("Funny mode")

secret_input = st.text_input("Enter replicate API key:", type="password")
if not secret_input:
    st.info("Please enter replicate token to continue.", icon="🗝️")
else:
    api = replicate.Client(api_token=secret_input)

    def get_flux_image(prompt: str):
        output = api.run("recraft-ai/recraft-v3",
                    input={
                        "size": "1365x1024",
                        "style": "any",
                        "prompt": prompt
                })
        return output

    # Function to handle user input
    def handle_input():
        user_input = st.session_state.user_input

        st.session_state.user_input = ""  # Clear input field after submitting

        if user_input:
            # Append user's message to the chat history
            st.session_state["messages"].append({
                "role": "user",
                "content": user_input
            })

            # Generate a response
            if checkbox_1:
                response = get_flux_image(
                    f"Make a very crazily funny version of {user_input}")
            else:
                response = get_flux_image(user_input)

            if response:
                # Append the response to the chat history
                st.session_state["messages"].append({
                    "role": "bot",
                    "content": response,
                })
            else:
                st.session_state["messages"].append({
                    "role":
                    "bot",
                    "content":
                    "An error occurred while generating the image.",
                })


    # Display chat messages from the history
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        else:
            image_url = message['content']
            response = requests.get(image_url)
            image_data = response.content
            st.write(f"**Assistant:** {image_url}")
            st.image(image_data)

    # Input box for user to type a message
    st.text_input("Type your message here:",
                key="user_input",
                on_change=handle_input)