import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 1. Page Configuration
st.set_page_config(page_title="OpenAI Q&A Bot", page_icon="🤖")
st.title("🤖 OpenAI & LangChain Q&A Bot")
st.write("Ask any question and get an instant response powered by GPT-4o-mini.")

# 2. Initialize the LangChain Model
# Streamlit will automatically look for the key in its secure Secrets settings
try:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
except Exception:
    st.error("Please configure your OPENAI_API_KEY in the Streamlit settings.")

# 3. Create the User Interface
with st.form("qa_form"):
    user_question = st.text_area(
        "Your Question:", 
        placeholder="e.g., What is the distance between the Earth and the Moon?"
    )
    submitted = st.form_submit_with_button("Ask Bot")

# 4. Handle Form Submission
if submitted:
    if not user_question.strip():
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("Thinking..."):
            try:
                # Define prompt
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful assistant providing clear and concise answers."),
                    ("user", "{question}")
                ])
                # Run chain
                chain = prompt | llm
                response = chain.invoke({"question": user_question})
                
                # Display Answer
                st.success("Answer:")
                st.write(response.content)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
