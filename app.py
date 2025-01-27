from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session management

# Simulated database
admins = {}
domains = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_signup', methods=['GET', 'POST'])
def admin_signup():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        password = request.form['password']
        
        if name in admins:
            return "Admin already registered."
        
        admins[name] = {'contact': contact, 'password': password}
        return redirect(url_for('admin_signin'))
    
    return render_template('admin_signup.html')

@app.route('/admin_signin', methods=['GET', 'POST'])
def admin_signin():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        if name in admins and admins[name]['password'] == password:
            session['logged_in'] = True
            session['admin_name'] = name
            return redirect(url_for('admin_dashboard'))
        
        return "Invalid credentials."
    
    return render_template('admin_signin.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin_signin'))
    
    return render_template('admin_dashboard.html', name=session.get('admin_name'))

@app.route('/register_domain', methods=['GET', 'POST'])
def register_domain():
    if not session.get('logged_in'):
        return redirect(url_for('admin_signin'))
    
    if request.method == 'POST':
        domain_name = request.form['domain_name']
        ip_address = request.form['ip_address']
        
        if domain_name in domains:
            return "Error: Domain already registered."
        
        domains[domain_name] = ip_address
        return "Domain registered successfully."
    
    return render_template('register.html')

@app.route('/update_domain', methods=['GET', 'POST'])
def update_domain():
    if not session.get('logged_in'):
        return redirect(url_for('admin_signin'))
    
    if request.method == 'POST':
        domain_name = request.form['domain_name']
        ip_address = request.form['ip_address']
        
        if domain_name in domains:
            domains[domain_name] = ip_address
            return "Domain updated successfully."
        
        return "Error: No such domain registered."
    
    return render_template('update.html')

@app.route('/resolve_domain', methods=['GET', 'POST'])
def resolve_domain():
    if request.method == 'POST':
        domain_name = request.form['domain_name']
        
        if domain_name in domains:
            return f"IP Address: {domains[domain_name]}"
        
        return "Domain not available."
    
    return render_template('resolve.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('admin_name', None)
    return redirect(url_for('admin_signin'))

if __name__ == '__main__':
    app.run(debug=True)
