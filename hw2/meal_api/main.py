from flask import Flask, render_template
from route_dish import dish_blueprint
from route_meal import meal_blueprint
from db import db
from werkzeug.exceptions import HTTPException
import dotenv
import os

app = Flask(__name__)  # initialize Flask
app.register_blueprint(dish_blueprint)
app.register_blueprint(meal_blueprint)


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return render_template("500_generic.html", e=e), 500


error_codes = [404, 422, 415, 500, 504]

for code in error_codes:
    app.errorhandler(code)(lambda e: e), code

app.config.from_object
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///meal_api.db"
)
print(app.config["SQLALCHEMY_DATABASE_URI"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG"] = True
db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    dotenv.load_dotenv()
    port = int(os.environ.get("PORT", 5001))
    host = os.environ.get("HOST", "0.0.0.0")
    app.run(debug=True, port=port, host=host)
