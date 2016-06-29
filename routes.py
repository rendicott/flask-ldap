# Requires:
# yum groupinstall "Development Tools"
# yum install python-pip
# yum install python-ldap
# yum install python-devel
# yum install openldap-devel
# pip install flask-login
# pip install wtforms
# pip install flask-ldap-login
# pip install flask_wtf
'''
nano /usr/lib/python2.7/site-packages/flask_ldap_login/forms.py
#### CHANGE
#from flask.ext.wtf import Form
from flask_wtf import Form

'''

from flask import Flask, request, render_template
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
#from wtforms import Form
#from wtforms import TextField
#from wtforms import PasswordField
from flask_ldap_login import LDAPLoginForm, LDAPLoginManager

from ldap_config import LDAP_SETTINGS


app = Flask(__name__)      
app.secret_key = 'dank warhammer'
login_manager = LoginManager(app)

users = {}

for key,val in LDAP_SETTINGS.iteritems():
    app.config[key] = val

login_manager = LoginManager(app)              # Setup a Flask-Login Manager
ldap_manager = LDAP3LoginManager(app)          # Setup a LDAP3 Login Manager.

# Declare an Object Model for the user, and make it comply with the
# flask-login UserMixin mixin.
class User(UserMixin):
    def __init__(self, dn, username, data):
        self.dn = dn
        self.username = username
        self.data = data

    def __repr__(self):
        return self.dn

    def get_id(self):
        return self.dn

# Declare a User Loader for Flask-Login.
# Simply returns the User if it exists in our 'database', otherwise
# returns None.
@login_manager.user_loader
def load_user(id):
    if id in users:
        return users[id]
    return None

# Declare The User Saver for Flask-Ldap3-Login
# This method is called whenever a LDAPLoginForm() successfully validates.
# Here you have to save the user, and return it so it can be used in the
# login controller.
@ldap_manager.save_user
def save_user(dn, username, data, memberships):
    user = User(dn, username, data)
    users[dn] = user
    return user

@app.route('/')
def home():
    # Redirect users who are not logged in.
    if not current_user or current_user.is_anonymous:
        return redirect(url_for('login'))

    return render_template_string('home.html')

@app.route('/about')
def about():
    # Redirect users who are not logged in.
    if not current_user or current_user.is_anonymous:
        return redirect(url_for('login'))
    
    return render_template('about.html')

@app.route('/login', methods=['GET','POST'])
def login():
    # Instantiate a LDAPLoginForm which has a validator to check if the user
    # exists in LDAP.
    form = LDAPLoginForm()

    if form.validate_on_submit():
        # Successfully logged in, We can now access the saved user object
        # via form.user.
        login_user(form.user) # Tell flask-login to log them in.
        return redirect('/')  # Send them home

    return render_template_string('login.html', form=form)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5001)
