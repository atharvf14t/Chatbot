from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages


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

checkpointer = InMemorySaver()
graph = StateGraph(ChatState)

#add node
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node',END)
chatbot = graph.compile(checkpointer=checkpointer)
