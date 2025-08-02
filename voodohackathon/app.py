from flask import Flask, render_template, request, redirect, url_for, session
from logic import users, tickets, Ticket, authenticate_user, add_ticket

app = Flask(__name__)
app.secret_key = "secret123"  # For session management

# ----------------- Home -----------------
@app.route('/')
def home():
    user = session.get("user")
    return render_template('index.html', user=user)

# ----------------- Login -----------------
@app.route('/login')
def login():
    return render_template('login.html', user=None)

@app.route('/api_login', methods=['POST'])
def api_login():
    username = request.form['username']
    password = request.form['password']
    user = authenticate_user(username, password)
    if user:
        session['user'] = {'username': user.username, 'role': user.role}
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

# ----------------- Logout -----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

# ----------------- Dashboard -----------------
@app.route('/dashboard')
def dashboard():
    user = session.get("user")
    if not user:
        return redirect(url_for('login'))

    if user['role'] == 'agent':
        return redirect(url_for('agent_dashboard'))
    elif user['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))

    # For normal user
    user_tickets = [t for t in tickets if t.user == user['username']]
    return render_template('dashboard.html', user=user, tickets=user_tickets)

# ----------------- Create Ticket -----------------
@app.route('/create-ticket')
def create_ticket():
    user = session.get("user")
    if not user:
        return redirect(url_for('login'))
    return render_template('create-ticket.html', user=user)

@app.route('/api_create_ticket', methods=['POST'])
def api_create_ticket():
    user = session.get("user")
    if not user:
        return redirect(url_for('login'))

    subject = request.form['subject']
    description = request.form['description']
    category = request.form['category']

    add_ticket(user['username'], subject, description, category)
    return redirect(url_for('dashboard'))

# ----------------- Agent Dashboard -----------------
@app.route('/agent-dashboard')
def agent_dashboard():
    user = session.get("user")
    if not user or user['role'] != 'agent':
        return redirect(url_for('login'))
    return render_template('agent-dashboard.html', user=user, tickets=tickets)

# ----------------- Admin Dashboard -----------------
@app.route('/admin-dashboard')
def admin_dashboard():
    user = session.get("user")
    if not user or user['role'] != 'admin':
        return redirect(url_for('login'))
    return render_template('admin-dashboard.html', user=user, tickets=tickets, users=users)

# ----------------- Run -----------------
if __name__ == '__main__':
    app.run(debug=True)
