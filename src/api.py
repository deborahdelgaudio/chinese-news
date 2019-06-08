import flask
from src.database.db_manager import DatabaseManager

app = flask.Flask(__name__)
app.config.from_pyfile('config/config.cfg')

with DatabaseManager(app.config) as db:
    record = db.execute_query("SELECT * FROM news LIMIT 1;")
    print(record)

@app.route('/')
def index():
    return "Hello Gabri!"

if __name__ == "__main__":
    app.run()