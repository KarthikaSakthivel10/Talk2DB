# Talk2DB
AI-Powered Natural Language Data Base Assistance

**Project Overview:**

-> Talk2DB is a natural language interface for SQL databases designed to simplify data access for non-technical users such as store owners and managers. 
-> The application allows users to query their data using plain English instead of SQL, and instantly receive answers, visualizations, and downloadable reports. It also enables data upload, preview, and automated chart generation—all within a streamlined interface.

**Tech Stack:**

- **Frontend:**
Streamlit: UI for query input, results display, and visualizations.

- **Backend:**
Python: Core logic for query processing and backend functions.

- **DataBase:**
MySQL: Database storing structured user and store data.

- **Libraries & Tools:**
-> Gemini (Google’s GenAI API): Converts natural language to SQL queries.
-> SQLAlchemy & bcrypt: Handles user authentication and database connections.
-> Pandas: Data handling and manipulation.
-> Matplotlib, Plotly: Visualization libraries for automated chart generation.
-> Sumy / Langchain (Optional): For summarizing insights in text form.

**Setup and Installation**

**Prerequisites:**
- Python 3.x
- MySQL Server
- Streamlit
- Git

**Installation:**

1. Clone the repository

2. Install backend dependencies:
_pip install -r requirements.txt_

3. Run the application using:
_streamlit run att.py_

**Features:**

- Natural Language to SQL: Ask questions in plain English and get accurate SQL-based results.
- Data Upload & Preview: Upload Excel files and preview data within the app.
- Automated Visualizations: Generate bar, pie, line, and donut charts based on uploaded or queried data.
- Insight Generation: Automatically generate summary insights from visualized data.
- User Authentication: Secure login and registration system using SQLAlchemy and bcrypt.
- Integrated Dashboard: Unified dashboard with visual insights, charts, and reports for store analysis.
