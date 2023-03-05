import streamlit as st
import openai
import os


def setup_openai_api():
    openai.api_key = os.environ.get('OPEN_AI_KEY')


def get_user_input():
    return st.text_area("質問", value="OpenAIとOpen AIの違いは？")


def generate_response(system_text, user_text):
    message = [{"role": "system", "content": system_text}, {"role": "user", "content": user_text}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        max_tokens=2000,
        temperature=0,
        stream=True
    )
    return response


def display_response(response):
    partial_words = ""
    answer = st.empty()
    for chunk in response:
        if chunk and "delta" in chunk["choices"][0] and "content" in chunk["choices"][0]["delta"]:
            partial_words += chunk["choices"][0]["delta"]["content"]
            answer.write(partial_words)


def main():
    setup_openai_api()

    system_text = "アシスタントAI"
    user_text = get_user_input()
    is_generate_clicked = st.button("回答")

    if is_generate_clicked:
        response = generate_response(system_text, user_text)
        display_response(response)


if __name__ == "__main__":
    main()
