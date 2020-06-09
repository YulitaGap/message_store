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


@app.route('/login', methods=["GET"])
def login():
    """
    Login processor function
    """
    return render_template("main/login.html")


# ############################# EXAMPLE CONTENT  ##########################
# ####### FROM OTHER PROJECT ################
class AuthTerminal:
    """ Authentication terminal for working with "users" database """

    def __init__(self, f_name="database/users.json"):
        """
        The init method. Set the basic parameters of the object.
        Parses the file for users.
        :param f_name: str - by default "users.json"
        """
        pass

    def verify(self, login, pasw):
        """
        Verify the user credentials
        :param login: str
        :param pasw: str
        :return: bool
        """
        try:
            return self.data[login]["pasw"] == pasw
        except KeyError:
            return False

    def user_permission(self, login, pasw):
        """
        Return user permission ("mdoer" or "admin").
        :param login: str
        :param pasw: str
        :return: bool
        """
        if self.verify(login, pasw):
            return self.data[login]["type"]
        else:
            return False

    def is_login_free(self, login):
        """
        Return if the login is not used
        :param login: str
        :return: bool
        """
        return login not in self.data

    def register(self, form):
        """
        Register new user if the form value is OK. Return the success of the
        operation.
        :param form: dict
        :return: bool
        """
        login = form["login"]
        del form["login"]
        if self.is_login_free(login) and form["type"] == "moder":
            self.data[login] = form
            self.up_to_date = False
            return True
        else:
            return False

    def confirm_access(self, login, pasw, m_id):
        """
        Validate access of the user to location modification.
        :param login: str
        :param pasw: str
        :param m_id: int
        :return: bool
        """
        if self.verify(login, pasw) and (self.data[login]["access"] == m_id or
                                         self.data[login]["type"] == "admin"):
            return True
        else:
            return False

    @staticmethod
    # TODO: delete this method
    def get_new_id():
        return 1


auth = AuthTerminal()


@app.route("/register", methods=["GET"])
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
