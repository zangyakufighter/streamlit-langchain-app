import streamlit as st

st.title("langchain-streamlit-app")

prompot = st.chat_input("What is up?")
# streamlitはファイル単位で上から下まで処理を再実行する
# print(prompot)

if prompot: # 入力された文字列がある
    with st.chat_message("user"): #ユーザーのアイコン
        st.markdown(prompot) # promptをマークダウンとして整形表示

    with st.chat_message("assistant"): # AIのアイコンで
        response = "こんにちは"
        st.markdown(response)

