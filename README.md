### Important Commands

Run the following commands in the terminal to get started:

- To install the libraries needed:
`pip install streamlit pandas sqlalchemy openpyxl`
- To initialise the database: `python seed.py`
- To run the application: `streamlit run app.py`

The first two only need to be executed only once, when you clone the repository, and the third one is used whenever you want to re-run the app.
### What these libraries are exactly

- Streamlit: This is the tool that instantly turns our underlying Python logic into the interactive web dashboard you see in your browser. Every time you click a button or add an expense, Streamlit redraws the screen to keep the data fresh.
- SQLite: When you run the seed.py script, it creates a file called `expenses.db` from the dataset we chose on kaggle. This is our local database, all the records are saved inside this single file on your own computer.
- SQLAlchemy: Databases only understand a specific language called SQL. SQLAlchemy automatically translates the actions you take on the Streamlit dashboard into the exact SQL commands needed to update the `expenses.db`.
- Pandas & Openpyxl: Pandas organizes the data into neat rows and columns so Streamlit can display it. `openpyxl` is just a small helper library that allows Pandas to read our initial `expenses_data.xlsx` file.

### Some Tips
- Keep the terminal open when running the app, because once you close it the dashboard stops working.
- Everything you add or change on the dashboard stays local, so you won't overwrite each other's test data when clicking around in the app.
- To stop the app press `CTRL + C` or `CMD + C` in the terminal.
