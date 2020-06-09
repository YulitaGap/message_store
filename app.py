from flask import Flask, render_template
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
