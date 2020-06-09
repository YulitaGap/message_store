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

@app.route('/add_account', methods=['GET'])
def add_acc_get():
        """
        render the page to add account
        """
        return render_template("user_side/add_account.html")

@app.route('/user_main', methods=['GET'])
def main_get():
        """
        render the main user page
        """
        return render_template("user_side/user_main.html")


@app.route('/create_order', methods=['GET'])
def create_order_get():
        """
        render the page to create order
        """
        return render_template("user_side/create_order.html")


@app.route('/view_statistics', methods=['GET'])
def statistics_get():
        """
        render the page to view statistics
        """
        return render_template("user_side/user_statistics.html")


@app.route('/view_catalogue', methods=['GET'])
def catalogue_get():
        """
        render the page to view catalogue
        """
        return render_template("main/view_template.html")


@app.route("/add_account", methods=["POST"])
def add_acc():
    """
    Try to add the account
    """
    login = request.form.get("login")
    pasw = request.form.get("pasw")
    social_network_id = request.form.get("social_network_id")

    if not login or not pasw or not  social_network_id:
        return redirect(url_for("fail", _method="GET"))
    query = {
        "principal_id": "",
        "social_network_id": social_network_id,
        "login": login,
        "password": pasw

    }
    if AddSocialNetworkAccount(query):
        return redirect(url_for("create_order", _method="GET"))
    else:
        return redirect(url_for("fail", _method="GET"))


# ############################ END OF EXAMPLE #############################
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
