import psycopg2
import pandas as pd
from shiny import App, render, reactive, ui

# Connect to PostgreSQL
def connect_to_db():
    conn = psycopg2.connect(
        host="localhost",     # Replace with your host
        database="",      # Replace with your database name
        user="",  # Replace with your username
        password=""  # Replace with your password
    )
    return conn


def fetch_table_data():
    conn = connect_to_db()
    query = "SELECT * FROM sales"  # Use your table name
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def insert_into_table(new_row):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Filter out empty or null values
    new_row = {k: v for k, v in new_row.items() if v}

    # Ensure `id` is not included if it's an auto-incrementing primary key and allow DB to create it
    if 'id' in new_row:
        del new_row['id']

    columns = ', '.join(new_row.keys())
    values = ', '.join(['%s'] * len(new_row))
    query = f"INSERT INTO sales ({columns}) VALUES ({values})"
    cursor.execute(query, list(new_row.values()))
    conn.commit()
    cursor.close()
    conn.close()


def update_table(row_id, updated_row):
    conn = connect_to_db()
    cursor = conn.cursor()
    set_clause = ', '.join([f"{key} = %s" for key in updated_row.keys()])
    query = f"UPDATE sales SET {set_clause} WHERE id = %s"
    cursor.execute(query, list(updated_row.values()) + [row_id])
    conn.commit()
    cursor.close()
    conn.close()

# Shiny UI
app_ui = ui.page_fluid(
    ui.output_table("table"),
    ui.input_action_button("refresh", "Refresh Data"),
    ui.input_text("new_data", "New Data (comma-separated)"),
    ui.input_action_button("add_row", "Add Row"),
    ui.input_numeric("update_id", "Row ID to Update", value=0),
    ui.input_text("update_data", "Updated Data (comma-separated including ID)"),
    ui.input_action_button("update_row", "Update Row"),
    ui.download_button("download_csv", "Download CSV")
)

def server(input, output, session):
    df = reactive.Value(fetch_table_data())

    @reactive.Effect
    @reactive.event(input.refresh)
    def _():
        df.set(fetch_table_data())

    @reactive.Effect
    @reactive.event(input.add_row)
    def _():
        if input.new_data():
            new_row = dict(zip(df().columns, input.new_data().split(',')))
            insert_into_table(new_row)
            df.set(fetch_table_data())

    @reactive.Effect
    @reactive.event(input.update_row)
    def _():
        if input.update_id() and input.update_data():
            updated_row = dict(zip(df().columns, input.update_data().split(',')))
            update_table(input.update_id(), updated_row)
            df.set(fetch_table_data())

    @output
    @render.table
    def table():
        return df()

    # Corrected download_csv function using a generator
    @render.download(filename="data.csv")
    def download_csv():
        # Use a generator to yield the CSV data
        csv_data = df().to_csv(index=False)
        yield csv_data

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
