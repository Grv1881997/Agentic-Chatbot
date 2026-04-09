import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json
import re


class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message,model=None):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message
        self.model = model

    def format_tavily_results(self, content, model=None):
        """
        Format Tavily search results using AI to present them naturally
        """
        try:
            # Try to parse as JSON
            if isinstance(content, str):
                results = json.loads(content)
            else:
                results = content
            
            # If we have a model, use AI to format the results naturally
            if model and isinstance(results, list):
                # Prepare a summary of the search results for the AI
                search_summary = "I found some search results for you. Here's what I discovered:\n\n"
                
                for i, result in enumerate(results, 1):
                    if isinstance(result, dict):
                        title = result.get('title', 'No Title')
                        url = result.get('url', '')
                        content_text = result.get('content', '')
                        score = result.get('score', 0)
                        
                        # Clean up content for AI processing
                        cleaned_content = re.sub(r'\s+', ' ', content_text).strip()
                        if len(cleaned_content) > 300:
                            cleaned_content = cleaned_content[:300] + "..."
                        
                        search_summary += f"{i}. {title}\n"
                        search_summary += f"   Content: {cleaned_content}\n"
                        search_summary += f"   Source: {url}\n\n"
                
                # Create AI prompt to format results naturally
                ai_prompt = f"""Based on these search results, please present them to the user in a natural, conversational way. 
                Start with a friendly introduction like "Here's what I found for you:" or "I found some great results for your search:".
                Then summarize the key findings in a clear, organized manner. Make it sound like a helpful assistant presenting information.
                
                IMPORTANT: Always include the source URLs in your response so users can visit the links. Format them as clickable links or clearly mention the URLs.
                
                {search_summary}
                
                Please format your response in a friendly, conversational tone and make sure to include all the URLs for each result."""
                
                try:
                    # Get AI to format the results
                    ai_response = model.invoke(ai_prompt)
                    return ai_response.content
                except Exception as e:
                    print(f"AI formatting failed: {e}")
                    # Fall back to manual formatting
                    return self._manual_format_results(results)
            
            # Fallback to manual formatting if no model or parsing fails
            return self._manual_format_results(results)
            
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error formatting results: {e}")
            # If parsing fails, return the original content with basic formatting
            return f"## Search Results\n\n{content}"

    def _manual_format_results(self, results):
        """
        Manual formatting as fallback
        """
        formatted_output = "## Search Results\n\n"
        
        if isinstance(results, list):
            for i, result in enumerate(results, 1):
                if isinstance(result, dict):
                    title = result.get('title', 'No Title')
                    url = result.get('url', '')
                    content_text = result.get('content', '')
                    score = result.get('score', 0)
                    
                    # Clean up content
                    cleaned_content = re.sub(r'\s+', ' ', content_text).strip()
                    if len(cleaned_content) > 500:
                        cleaned_content = cleaned_content[:500] + "..."
                    
                    formatted_output += f"### {i}. {title}\n\n"
                    formatted_output += f"**URL:** {url}\n\n"
                    formatted_output += f"**Content:** {cleaned_content}\n\n"
                    formatted_output += f"**Relevance Score:** {score:.2f}\n\n"
                    formatted_output += "---\n\n"
        
        return formatted_output

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
                            #st.write("Tool Call Start")
                            # Format the tool content for better readability using AI
                            formatted_content = self.format_tavily_results(message.content, self.model)
                            st.markdown(formatted_content, unsafe_allow_html=True)
                            #st.write("Tool Call End")
                        st.session_state["chatbot_with_web_history"].append({"role": "tool", "content": formatted_content})
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