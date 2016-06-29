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

from ldap_config import LDAP

app = Flask(__name__)      
app.secret_key = 'dank warhammer'
login_manager = LoginManager(app)

users = {}

app.config.update(LDAP=LDAP)
ldap_mgr = LDAPLoginManager(app)

@ldap_mgr.save_user
def save_user(username, userdata):
    users[username] = User(username, userdata)
    return users[username]

class User(UserMixin):
    def __init__(self):
        pass

#class LoginForm(Form):
#    username = TextField('Username')
#    password = PasswordField('Password')
#    def validate_on_submit(self):
#        return True

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')
 
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def ldap_login():

    form = LDAPLoginForm(request.form)
    if form.validate_on_submit():
        login_user(form.user, remember=True)
        print "Valid"
        return redirect('/')
    else:
        print "Invalid"
    return render_template('login.html', form=form)

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5001)
