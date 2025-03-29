import streamlit as st

st.title("langchain-streamlit-app")

# streamlitはファイル単位で上から下まで処理を再実行する
# １画面の中で画面のリロードをまたいで入力値を引き渡すにはセッション変数stに値を格納する
if "messages" not in st.session_state: # st.session_state に messagesがない場合
    st.session_state.messages = [] # st.session_state.messsages を空のリストで初期化

for messages in st.session_state.messages: # st.session_state.messagesでループ
    with st.chat_message(messages["role"]):
        st.markdown(messages["content"])

prompt = st.chat_input("What is up?")

if prompt: # 入力された文字列がある
    with st.chat_message("user"): #ユーザーのアイコン
        st.markdown(prompt) # promptをマークダウンとして整形表示

    # ユーザの入力内容をst.session_state.messsages に追加
    st.session_state.messages.append({"role":"user", "content":prompt})

    with st.chat_message("assistant"): # AIのアイコンで
        response = "こんにちは"
        st.markdown(response)
    
    # 応答を st.session_state.messsages に追加
    st.session_state.messages.append({"role":"assistant", "content":response})

