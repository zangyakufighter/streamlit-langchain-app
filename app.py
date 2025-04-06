import os

import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models.openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
from langchain.memory import ConversationBufferMemory
from langchain.prompts import MessagesPlaceholder

def create_agent_chain():
    chat = ChatOpenAI(
        model_name=os.environ["OPENAI_API_MODEL"],
        temperature=os.environ["OPENAI_API_TEMPERATURE"],
        streaming=True,
    )

    # OpenAI Functions AgentのプロンプトにMemoryの会話履歴を追加するための設定
    agent_kwargs = {
        "extra_prompt_messages" : [MessagesPlaceholder(variable_name="memory")]
    }
    # OpenAI Functions Agentが使える設定でMemoryを初期化
    memory = ConversationBufferMemory(memory_key="memory", return_messages=True)

    tools = load_tools(["ddg-search", "wikipedia"])
    return initialize_agent(
        tools, 
        chat, 
        agent=AgentType.OPENAI_FUNCTIONS,
        agent_kwargs=agent_kwargs, #追加
        memory=memory) #追加

load_dotenv()

st.title("langchain-streamlit-app")

# streamlitはファイル単位で上から下まで処理を再実行する
# １画面の中で画面のリロードをまたいで入力値を引き渡すにはセッション変数stに値を格納する
if "messages" not in st.session_state: # st.session_state に messagesがない場合
    st.session_state.messages = [] # st.session_state.messsages を空のリストで初期化

if "agent_chain" not in st.session_state:
    st.session_state.agent_chain = create_agent_chain()

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

        callback = StreamlitCallbackHandler(st.container())
        # st.session_stateから取り出したagent_chainを使うようにする
        response = st.session_state.agent_chain.run(prompt, callbacks=[callback])
        st.markdown(response)
    
    # 応答を st.session_state.messsages に追加
    st.session_state.messages.append({"role":"assistant", "content":response})

