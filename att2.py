import streamlit as st
from streamlit_option_menu import option_menu
from sqlalchemy import create_engine, text
import pandas as pd
import bcrypt
import google.generativeai as genai  # Using Google Gemini API
import pymysql
from urllib.parse import quote_plus
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from autoviz.AutoViz_Class import AutoViz_Class
from sqlalchemy import create_engine, text
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd
import google.generativeai as genai

from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # Load environment variables from .env
API_KEY = "AIzaSyCW9nyftYZNWXCOifcE1xlcRDynIGI1KkE"
genai.configure(api_key=API_KEY)

# Database Credentials
DB_USER = "root"
DB_PASSWORD = quote_plus("Kar@mysql#10")  # Encode special characters
DB_HOST = "127.0.0.1"
DB_NAME = "talk2db"

# Secure connection to MySQL using SQLAlchemy
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL)


# Function to hash passwords securely
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Function to check if the entered password matches the stored hash
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Function to create a new user in the database
def create_user(username, password):
    hashed_pw = hash_password(password)
    query = text("INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)")
    with engine.begin() as conn:
        conn.execute(query, {"username": username, "password_hash": hashed_pw})
    return True

# Function to authenticate the user during login
def authenticate_user(username, password):
    query = text("SELECT password_hash FROM users WHERE username = :username")
    with engine.begin() as conn:
        result = conn.execute(query, {"username": username}).fetchone()
    if result and check_password(password, result[0]):
        return True
    return False

# Function to generate SQL queries from user questions using Gemini API
# def get_sql_query(user_question):
#     try:
#         model = genai.GenerativeModel("gemini-pro")
#         response = model.generate_content(f"Convert this to an optimized SQL query: {user_question}")
#         return response.text.strip()
#     except Exception as e:
#         return f"Error generating SQL: {str(e)}"

def get_sql_query(user_question):
    try:
        model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
        response = model.generate_content(user_question)
        return response.text.strip()
    except Exception as e:
        return f"Error generating SQL: {str(e)}"
    
def fetch_query_results(sql_query):
    try:
        df = pd.read_sql(sql_query, engine)
        return df
    except Exception as e:
        return f"Error: {str(e)}"
    

# Function to execute SQL query and fetch results
# def fetch_query_results(sql_query):
#     try:
#         df = pd.read_sql(sql_query, engine)
#         return df
#     except Exception as e:
#         return f"Error: {str(e)}"

# Streamlit UI Configuration
st.set_page_config(page_title="Talk to DB", layout="wide")

if "selected" not in st.session_state:
    st.session_state.page = "home"
if "df" not in st.session_state:
    st.session_state.df = None
if "generated_charts" not in st.session_state:
    st.session_state.generated_charts = set()
if "autoviz_run" not in st.session_state:
    st.session_state.autoviz_run = False
if "report_content" not in st.session_state:
    st.session_state.report_content = []
if "dashboard_charts" not in st.session_state:
    st.session_state.dashboard_charts = []

def rename_duplicate_columns(df):
    cols = pd.Series(df.columns)
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [dup + '_' + str(i) if i != 0 else dup for i in range(sum(cols == dup))]
    df.columns = cols
    return df

# Sidebar Navigation
with st.sidebar:
    selected = option_menu("Talk to DB", ["Home", "Sign Up", "Login", "Q/A Page", "Upload and Preview", "Visualizations", "Dashboard", "AutoViz"],
                           icons=["house", "person-plus", "box-arrow-in-right", "chat-text", "table", "bar-chart", "graph-up", "robot", "file-earmark-excel"],
        menu_icon="database", 
        default_index=0)

# Home Page
def home():
    st.image(r"C:\\Users\\Karthika\\Documents\\Talk2db\\T2DBapp\\unnamed.gif", width=500)
    st.title("Welcome to Talk to DB 🗃️")
    st.write("""
        **Talk to DB** is an AI-powered tool that allows users to interact with databases using natural language.
        
        🔹 Convert human language to SQL queries effortlessly.
        
        🔹 Get instant results with explanations.
        
        🔹 Download your data in an easy-to-use format.
        
        🔹 Visualize your data and view Dashboards instantly
        
        **Sign up now and experience the future of database interaction and sales insights!**
    """)

# Sign Up Page
def signup():
        st.title("Create an Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            if username and password:
                create_user(username, password)
                st.success("Account created successfully! Please log in.")
            else:
                st.error("Username and password cannot be empty!")

# Login Page
def login():
        st.title("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate_user(username, password):
                st.success("Login successful!")
            else:
                st.error("Invalid credentials.")
            
# Q/A Page
def qa():
        st.title("Query your Database")
        query = st.text_area("Ask your question in natural language")
        if st.button("Generate SQL Query & Fetch Data"):
            sql_query = get_sql_query(query)
            st.success(f"Generated Query: {sql_query}")
            data = fetch_query_results(sql_query)
            if isinstance(data, pd.DataFrame):
                st.dataframe(data)
            else: 
                st.error(data)
                
# def sql_to_excel_page():
#     st.title("🧾 SQL to Excel Converter")
#     st.write("Write your SQL query below and download the result as an Excel file.")

#     sql_input = st.text_area("Enter your SQL Query")

#     if st.button("Run Query"):
#         if sql_input.strip() == "":
#             st.warning("Please enter a valid SQL query.")
#             return
#         try:
#             df = pd.read_sql(sql_input, engine)
#             if df.empty:
#                 st.warning("Query executed successfully, but returned no results.")
#             else:
#                 st.success("Query executed successfully!")
#                 st.write("### Query Result Preview:")
#                 st.dataframe(df)

#                 # Save to Excel and prepare download
#                 excel_file = df.to_excel(index=False, engine='openpyxl')
#                 st.download_button(
#                     label="Download as Excel",
#                     data=excel_file,
#                     file_name="query_result.xlsx",
#                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#                 )
#         except Exception as e:
#             st.error(f"Error executing query: {e}")

                
            
def upload_and_preview():
        st.write("## Upload your CSV/Excel file")
        uploaded_file = st.file_uploader("Upload your file", type=['csv', 'xlsx'])

        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')): 
                df = pd.read_excel(uploaded_file)

            df = rename_duplicate_columns(df)
            st.session_state.df = df

        if st.session_state.df is not None:
            st.write("### Dataset Preview")
            st.write(st.session_state.df.head())
            st.write("### Dataset Information")
            st.write(st.session_state.df.describe())
            
        
def generate_insight_for_bar_chart(df, x_axis, y_axis):
        highest_value = df[y_axis].max()
        highest_category = df[df[y_axis] == highest_value][x_axis].values[0]

        insight_text = (
            f"It appears that high values in {y_axis} are associated with {x_axis} variations. "
            f"Some notable patterns are that the highest value in {y_axis} corresponds to {highest_category} in {x_axis}. "
            "This might indicate a trend worth further analysis."
        )
        st.session_state.report_content.append(insight_text)
        return insight_text
    
def generate_insight_for_pie_chart(df, categorical_col):
        highest_frequency_category = df[categorical_col].value_counts().idxmax()
        highest_frequency = df[categorical_col].value_counts().max()

        insight_text = (
            f"It appears that the highest frequency in {categorical_col} is for '{highest_frequency_category}', "
            f"with {highest_frequency} occurrences. This may highlight a dominant category that could warrant further focus."
        )
        st.session_state.report_content.append(insight_text)
        return insight_text

def visualization_and_text_gen():
        if st.session_state.df is None:
            st.error("Please upload a dataset first.")
            return
        
        st.write("### Data Visualizations")
        chart_type = st.selectbox("Select a chart type", ("Bar Chart", "Pie Chart", "Donut Chart"))
        df = st.session_state.df
        
        if chart_type == "Bar Chart":
            x_axis = st.selectbox("Select X-axis", df.columns)
            y_axis = st.selectbox("Select Y-axis", df.columns)
            chart_id = (chart_type, x_axis, y_axis)

            if x_axis and y_axis and chart_id not in st.session_state.generated_charts:
                fig = px.bar(df, x=x_axis, y=y_axis, color=x_axis, color_continuous_scale=px.colors.sequential.Plasma)
                st.plotly_chart(fig)
                st.session_state.generated_charts.add(chart_id)
                st.session_state.dashboard_charts.append(fig)

                insight_text = generate_insight_for_bar_chart(df, x_axis, y_axis)
                st.write("**Generated Insight**")
                st.write(insight_text)
                
        elif chart_type == "Pie Chart" or chart_type == "Donut Chart":
            categorical_col = st.selectbox("Select Categorical Column", df.select_dtypes(include=['object']).columns)
            chart_id = (chart_type, categorical_col)
            
            if categorical_col and chart_id not in st.session_state.generated_charts:
                fig = px.pie(df, names=categorical_col, hole=0.4 if chart_type == "Donut Chart" else 0)
                st.plotly_chart(fig)
                st.session_state.generated_charts.add(chart_id)
                st.session_state.dashboard_charts.append(fig)

                insight_text = generate_insight_for_pie_chart(df, categorical_col)
                st.write("**Generated Insight**")
                st.write(insight_text)
            
        if st.session_state.report_content:
            st.write("### Generated Text Report")
            for report in st.session_state.report_content:
                st.write(report)

            st.download_button(
                label="Download Report as Text File",
                data="\n\n".join(st.session_state.report_content),
                file_name="analysis_report.txt",
                mime="text/plain"
            )

            st.download_button(
                label="Download Report as Word File",
                data="\n\n".join(st.session_state.report_content),
                file_name="analysis_report.doc",
                mime="text/plain"
            )
            

def dashboard_page():
        st.write("### Dashboard - Visualized Charts with Insights")
        if not st.session_state.dashboard_charts:
            st.write("No charts have been added to the dashboard yet. Go to the Visualizations page to create charts.")
        else:
            for i, chart in enumerate(st.session_state.dashboard_charts):
                # Display each chart
                st.plotly_chart(chart)
                
                # Display the corresponding insight text below each chart
                if i < len(st.session_state.report_content):
                    st.write("**Insight for this chart:**")
                    st.write(st.session_state.report_content[i])
                    
                
def autoviz_page(df):
        if df is None:
            st.error("Please upload a dataset first.")
            return

        if st.checkbox("Run AutoViz for Automated EDA"):
            st.write("Auto-generated Visualizations")
            AV = AutoViz_Class()
            df_av = AV.AutoViz(
                filename="",
                sep=",",
                depVar="",
                dfte=df,
                header=0,
                verbose=0,
                lowess=False,
                chart_format="png",
                max_rows_analyzed=150000,
                max_cols_analyzed=30,
            )
            for fig in plt.get_fignums():
                st.pyplot(plt.figure(fig))
            
            st.session_state.autoviz_run = True
            
def main():
    
    if selected == "Home":
        home()
    elif selected == "Sign Up":
        signup()
    elif selected == "Login":
        login()
    elif selected == "Q/A Page":
        qa()
    elif selected == "Upload and Preview":
        upload_and_preview()
    elif selected == "Visualizations":
        visualization_and_text_gen()
    elif selected == "Dashboard":
        dashboard_page()
    elif selected == "AutoViz":
        autoviz_page(st.session_state.df)

if __name__ == "__main__":
    main()





















