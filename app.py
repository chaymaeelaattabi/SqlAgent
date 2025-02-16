import re
import io
import sys

import os
from dotenv import load_dotenv

import streamlit as st

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text

from langchain.sql_database import SQLDatabase
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.agents import AgentType, create_sql_agent
from langchain.agents.agent_toolkits.sql.toolkit import SQLDatabaseToolkit



azure_deployment=os.getenv("OPENAI_CHAT_MODEL")
openai_api_base= os.getenv("OPENAI_API_BASE")
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_type =os.getenv("OPENAI_API_TYPE")
openai_api_version = os.getenv("OPENAI_API_VERSION", "2023-07-01-preview")

DATABASE_URL = "sqlite:///school.db"


engine = create_engine(DATABASE_URL)
Base = declarative_base()


class Parent(Base):
    __tablename__ = 'parents'
    id = Column(Integer, primary_key=True)
    student_name = Column(String(20), default='')
    parent_name = Column(String(20))
    parent_mobile = Column(String(10))
    address = Column(String(100)) 

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))  
    score = Column(Integer)
    teacher_note = Column(Text)
    class_name = Column(String(10))  

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    subject = Column(String(20))  

Session = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(engine)
    with Session() as session:
        parents = [
            Parent(student_name='Alex', parent_name='Barry', parent_mobile='0881234567', address='123 Main St'),
            Parent(student_name='Alice', parent_name='Jessica', parent_mobile='0891234567', address='456 Elm St'),
            Parent(student_name='Jack', parent_name='Simon', parent_mobile='0876666666', address='789 Oak St'),
            Parent(student_name='Ophelia', parent_name='Tracy', parent_mobile='0881111111', address='321 Pine St')
        ]

        students = [
            Student(name='Alex', score=100, teacher_note='Alex did perfectly every day in the class. There is no surprise he got the full mark.', class_name='Math'),
            Student(name='Alice', score=70, teacher_note='Alice needs a lot of improvements.', class_name='English'),
            Student(name='Jack', score=75, teacher_note='Even it\'s not the best, Jack has already improved. Keep going.', class_name='Science'),
            Student(name='Ophelia', score=0, teacher_note='Unfortunately, Ophelia missed the test.', class_name='Math'),
            Student(name='Zack', score=60, teacher_note='Zack needs to do better.', class_name='History')
        ]
        
        teachers = [
            Teacher(name='Mr. Johnson', subject='Math'),
            Teacher(name='Ms. Smith', subject='English'),
            Teacher(name='Mr. Brown', subject='Science'),
            Teacher(name='Ms. White', subject='History')
        ]
        
        session.add_all(parents)
        session.add_all(students)
        session.add_all(teachers)
        session.commit()



init_db()


db = SQLDatabase(engine)  
llm = AzureChatOpenAI(azure_deployment=azure_deployment,
                      openai_api_base=openai_api_base,
                      openai_api_key=openai_api_key, 
                      openai_api_type=openai_api_type,
                      openai_api_version=openai_api_version,
                      temperature=0)


final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", 
         """
          You are a helpful AI assistant expert in querying SQL Database to find answers to user's question about students, parents and teachers.
         """
         ),
        ("user", "{question}\n ai: "),
    ]
)




sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_toolkit.get_tools()

print (sql_toolkit.get_tools())
sqldb_agent = create_sql_agent(
    llm=llm,
    toolkit=sql_toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #handle_parsing_errors=True,
    verbose=True
)


def remove_ansi_escape_sequences(text):
    ansi_escape_pattern = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape_pattern.sub('', text)

log_buffer = io.StringIO()
original_stdout = sys.stdout
sys.stdout = log_buffer
# Set page config  
st.set_page_config(page_title="Talk to your DB", page_icon="🗣️", layout="wide")  
  
# Custom CSS to inject into the page for styling  
st.markdown("""  
<style>  
    .app-title {  
        font-weight: bold;  
        color: #0e1117;  
        font-size: 2em;  
    }  
    .input-prompt-container {  
        padding: 1em 0;  
    }  
    .response-container {  
        margin-top: 1em;  
    }  
    .app-logo {  
        max-height: 40px;  
        margin-right: 10px;  
    }  
    .header-container {  
        display: flex;  
        align-items: center;  
    }  
    .query-button {  
        margin-top: 10px;  
    }  
    .agent-logs, .response-display {  
        background-color: #f0f2f6;  
        border-radius: 5px;  
    }  
    .footer {  
        margin-top: 2em;  
        font-style: italic;  
    }  
</style>  
""", unsafe_allow_html=True)  
  
# App header with logos  
st.markdown("""  
<div class="header-container">  
    <img src="https://scontent.fmad8-1.fna.fbcdn.net/v/t1.6435-9/84047081_2853162711418244_5950541033849749504_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=5f2048&_nc_ohc=_I5TO3E-p6gAX9kKBjE&_nc_ht=scontent.fmad8-1.fna&oh=00_AfBgA8QP8EoY9zMdFObziMG5HrCHSVDIPFEQxVq7ELwWug&oe=66202949" alt="System Logo" class="app-logo"/>
    <div class="app-title">Talk to your Database</div>  
      
</div>  
""", unsafe_allow_html=True)  
  
# Input prompt  
input_prompt = st.text_input("Input Prompt:", key="input", placeholder="Type your question here...")  
  
submit = st.button("Submit Your Query", key="submit") 
  
# Process query  
if submit:  
    with st.spinner("Processing your query..."):  
        try:  
            sys.stdout = log_buffer  
            # Mockup response, replace with actual database query logic  
            response = sqldb_agent.run(final_prompt.format(question=input_prompt)) 
            sys.stdout = original_stdout  
            logs = log_buffer.getvalue()  
            clean_logs = remove_ansi_escape_sequences(logs)  
  
            st.subheader("Logs:")  
            st.text_area("Agent Logs", value=clean_logs, height=300, key="logs")  
    
            st.subheader("The Response is:")  
            st.text_area("Response", value=response, height=150, key="response")  
              
        except Exception as e:  
            sys.stdout = original_stdout  
            st.error(f"An error occurred: {e}")  
        finally:  
            sys.stdout = original_stdout  
            log_buffer.truncate(0)  
            log_buffer.seek(0)  
  
st.markdown("---")  
st.markdown("<div class='footer'>Enter your natural language question above and press 'Submit Your Query' to get a response.</div>", unsafe_allow_html=True)  




