from flask import Flask, render_template, request
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


@app.route('/view_user_catalogue', methods=['POST', 'GET'])
def user_catalogue_get():
    """
    render the page to view user catalogue
    """
    return render_template("user_side/user_catalogue.html")

@app.route('/view_author_catalogue', methods=['POST', 'GET'])
def author_catalogue_get():
    """
    render the page to view catalogue
    """
    return render_template("author_side/author_catalogue.html")


@app.route('/view_catalogue', methods=['POST', 'GET'])
def catalogue_get():
    """
    render the page to view catalogue
    """
    return render_template("main/view_template.html",
                           query_index=request.args['index'])


# Author navigation routes
@app.route('/author_main', methods=['GET'])
def author_main_get():
    """
    render the main author page
    """
    return render_template("author_side/author_main.html")


@app.route('/update_price', methods=['GET'])
def update_price_get():
    """
    render the update price page
    """
    return render_template("author_side/update_price.html")


@app.route('/start_sale', methods=['GET'])
def start_sale_get():
    """
    render the page for starting page
    """
    return render_template("author_side/start_sale.html")


@app.route('/view_author_statistics', methods=['GET'])
def author_statistics_get():
    """
    render the page to view statistics
    """
    return render_template("author_side/author_statistics.html")


# ############################ END OF EXAMPLE #############################
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
