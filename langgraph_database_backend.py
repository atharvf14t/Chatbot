from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
load_dotenv()


llm= ChatOpenAI()


def chat_node(state: ChatState):
    #take user input from state
    messages=state['messages']

    #send to llm
    response = llm.invoke(messages)

    #response store state
    return {'messages': [response]}


conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

# checkpointer
checkpointer = SqliteSaver(conn=conn)
graph = StateGraph(ChatState)

#add node
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node',END)
chatbot = graph.compile(checkpointer=checkpointer)


def retrieve_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    return list(all_threads)




    
# print(f"Existing threads in database: {all_threads}")
#test

# response = chatbot.invoke(
#                 {'messages': [HumanMessage(content='Hi, what is my name')]}, 
#                 config={'configurable': {'thread_id': 'thread_1'}},
#             )

# print(response['messages'][-1].content)