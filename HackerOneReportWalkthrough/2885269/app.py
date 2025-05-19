from flask import Flask, render_template, request, redirect, session, url_for
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'secret-key'

# In-memory databases
users = {}
invitations = {}  # email -> role

@app.route('/')
def index():
    return render_template('index.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        session['email'] = email

        # Register user with default "member" role
        users[email] = {'email': email, 'role': 'member'}

        # Check if there's an invitation
        if email in invitations:
            users[email]['role'] = invitations[email]
            del invitations[email]

        return redirect(url_for('dashboard'))

    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect('/')
    user = users[session['email']]
    return render_template('dashboard.html', user=user)

@app.route('/invite', methods=['GET', 'POST'])
def invite():
    if 'email' not in session:
        return redirect('/')

    inviter = users[session['email']]
    if inviter['role'] != 'owner':
        return "Only owners can invite.", 403

    if request.method == 'POST':
        invited_email = request.form['email']
        role = request.form['role']
        invitations[invited_email] = role
        return f"Invited {invited_email} as {role}"

    return render_template('invite.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)