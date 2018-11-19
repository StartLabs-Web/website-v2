from flask import Flask, render_template
app = Flask(__name__)

# Index Page
@app.route('/new')
def new_version():
    return render_template('index.html')

# Old version of Startlabs Website
@app.route('/')
def old_version():
    return render_template('old/indexold.html')

@app.route('/email')
def old_email():
    return render_template('old/email.html')

if __name__ == '__main__':
    app.run(debug=True)

