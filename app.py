from flask import Flask, render_template, redirect, url_for, request
from flask_restful import Api

from modules.api_endpoints import *

app = Flask(__name__, static_url_path='/static')
api = Api(app, prefix="/api")
app.config['TEMPLATES_AUTO_RELOAD'] = True

for endpoint in ENDPOINTS_LIST:
    api.add_resource(endpoint, endpoint.ROUTE)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    """
    Login processor function
    """
    return render_template("main/login.html")


@app.route("/register", methods=["POST", "GET"])
def register_get():
    """
    render the register page
    """
    return render_template("main/register.html")


# #########################################################################


@app.route("/register_demo", methods=["POST"])
def register():
    """
    Try to register the user
    """
    user = request.form.get("login")
    pasw = request.form.get("pasw")

    if not user or not pasw:
        return redirect(url_for("fail", _method="GET"))

    email = request.form.get("email")
    name = request.form.get("name")
    phone = request.form.get("phone")
    company = request.form.get("company")
    query = {
        "login": user,
        "id": auth.get_new_id(),
        "type": "moder",
        "full_name": name,
        "mob_numb": phone,
        "email": email,
        "company": company,
        "pasw": pasw,
        "access": []
    }
    if auth.register(query):
        return redirect(url_for("login", _method="GET"))
    else:
        return redirect(url_for("fail", _method="GET"))


@app.route('/check_username', methods=["POST"])
def check_username():
    """
    Secondary function to check if the login if available
    :return: bool
    """
    username = request.args.get("username")
    return '1' if auth.is_login_free(username) else '0'


@app.route('/auten', methods=["POST", "GET"])
def auten():
    """
    Authenticate the user login
    """
    user = request.args.get("login")
    pasw = request.args.get("pasw")
    print()
    print(user, pasw)
    print()
    if user and pasw and auth.verify(user, pasw):
        # "Success!"
        permission = auth.user_permission(user, pasw)
        print(permission)
        if permission != "admin":
            return redirect(url_for("form_submit", user=user, pasw=pasw))
        else:
            return redirect(url_for("admin", user=user, pasw=pasw))
    else:
        return redirect(url_for("login", fail=True, _method="GET"))


@app.route('/fail', methods=['GET'])
def fail():
    """ Render Fail template """
    return render_template("main/fail.html")


# ############################ END OF EXAMPLE #############################
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
