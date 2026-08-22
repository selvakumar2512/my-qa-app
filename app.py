import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

st.set_page_config(page_title="Free Q&A Bot", page_icon="🤖")
st.title("🤖 Free & Fast Q&A Bot")

try:
    # Uses Llama 3 on Groq infrastructure (Completely Free Tier)
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)
except Exception:
    st.error("Please configure your GROQ_API_KEY in Streamlit settings.")

with st.form("qa_form"):
    user_question = st.text_area("Your Question:", placeholder="e.g., Explain gravity like I am 5.")
    submitted = st.form_submit_button("Ask Bot")

if submitted:
    if not user_question.strip():
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("Thinking..."):
            try:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a helpful assistant providing clear answers."),
                    ("user", "{question}")
                ])
                chain = prompt | llm
                response = chain.invoke({"question": user_question})
                st.success("Answer:")
                st.write(response.content)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
