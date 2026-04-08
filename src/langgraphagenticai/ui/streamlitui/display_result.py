import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase= self.usecase
        graph = self.graph
        user_message = self.user_message
        print(user_message)
        # Initialize or retrieve the chat history
        # if "chat_history" not in st.session_state:
        #     st.session_state["chat_history"] = []

        # # Add the user's message to the chat history
        # st.session_state["chat_history"].append({"role": "user", "content": user_message})
        print("Usecase Selected:", usecase)
        if usecase =="Basic Chatbot":
                # Initialize or retrieve the chat history for Basic Chatbot
                if "basic_chatbot_history" not in st.session_state:
                    st.session_state["basic_chatbot_history"] = []

                # Display the Basic Chatbot history
                # for chat in st.session_state["basic_chatbot_history"]:
                #     if chat["role"] == "user":
                #         with st.chat_message("user"):
                #             st.write(chat["content"])
                #     elif chat["role"] == "assistant":
                #         with st.chat_message("assistant"):
                #             st.write(chat["content"])

                if self.user_message:
                    # Add the user's message to the Basic Chatbot history
                    st.session_state["basic_chatbot_history"].append({"role": "user", "content": self.user_message})
                    print(user_message)
                    with st.chat_message("user"):
                        st.write(user_message)
                    for event in graph.stream({'messages':("user",user_message)}):
                        print(event.values())
                        for value in event.values():
                            # print(value['messages'])
                            # with st.chat_message("user"):
                            #     st.write(user_message)
                            assistant_message = value["messages"].content
                            with st.chat_message("assistant"):
                                st.write(assistant_message)
                            # Add the assistant's response to the chat history
                            st.session_state["basic_chatbot_history"].append({"role": "assistant", "content": assistant_message})


        elif usecase=="Chatbot With Web":
            # Initialize or retrieve the chat history for Chatbot With Web
            if "chatbot_with_web_history" not in st.session_state:
                st.session_state["chatbot_with_web_history"] = []

            # Display the Chatbot With Web history
            # for chat in st.session_state["chatbot_with_web_history"]:
            #     if chat["role"] == "user":
            #         with st.chat_message("user"):
            #             st.write(chat["content"])
            #     elif chat["role"] == "assistant":
            #         with st.chat_message("assistant"):
            #             st.write(chat["content"])
            #     elif chat["role"] == "tool":
            #         with st.chat_message("ai"):
            #             st.write("Tool Call Start")
            #             st.write(chat["content"])
            #             st.write("Tool Call End")

            # Add new user input to the Chatbot With Web history
            if self.user_message:
                # Add the user's message to the Chatbot With Web history (only once)
                if not st.session_state["chatbot_with_web_history"] or \
                        st.session_state["chatbot_with_web_history"][-1]["content"] != self.user_message:
                    st.session_state["chatbot_with_web_history"].append({"role": "user", "content": self.user_message})

                # Prepare state and invoke the graph
                #initial_state = {"messages": [user_message]}
                initial_state = {
                    "messages": [HumanMessage(content=user_message)]
                }
                print("Invoking graph with state:", initial_state)
                with st.chat_message("user"):
                    st.write(user_message)
                res = graph.invoke(initial_state)
                for message in res['messages']:
                    # if type(message) == HumanMessage:
                    #     # with st.chat_message("user"):
                    #     #     st.write(message.content)
                    #     st.session_state["chatbot_with_web_history"].append({"role": "user", "content": message.content})

                    if type(message)==ToolMessage:
                        with st.chat_message("ai"):
                            st.write("Tool Call Start")
                            st.write(message.content)
                            st.write("Tool Call End")
                        st.session_state["chatbot_with_web_history"].append({"role": "tool", "content": message.content})
                    elif type(message)==AIMessage and message.content:
                        with st.chat_message("assistant"):
                            st.write(message.content)
                        st.session_state["chatbot_with_web_history"].append({"role": "assistant", "content": message.content})
                    # final_ai_message = None

                    # for message in res['messages']:
                    #     if isinstance(message, AIMessage) and message.content:
                    #         final_ai_message = message  # keep updating → last one = final answer

                    # if final_ai_message:
                    #     with st.chat_message("assistant"):
                    #         st.write(final_ai_message.content)

                    #     st.session_state["chatbot_with_web_history"].append({
                    #         "role": "assistant",
                    #         "content": final_ai_message.content
                    #     })

           
                        

        elif usecase == "AI News":
            frequency = self.user_message
            with st.spinner("Fetching and summarizing news... ⏳"):
                result = graph.invoke({"messages": frequency})
                try:
                    # Read the markdown file
                    AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()

                    # Display the markdown content in Streamlit
                    st.markdown(markdown_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

        # Display the chat history
        # for chat in st.session_state["chat_history"]:
        #     if chat["role"] == "user":
        #         with st.chat_message("user"):
        #             st.write(chat["content"])
        #     elif chat["role"] == "assistant":
        #         with st.chat_message("assistant"):
        #             st.write(chat["content"])
        #     elif chat["role"] == "tool":
        #         with st.chat_message("ai"):
        #             st.write("Tool Call Start")
        #             st.write(chat["content"])
        #             st.write("Tool Call End")