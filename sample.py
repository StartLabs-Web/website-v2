from flask import Flask, render_template

app = Flask(__name__)

# Index Page
@app.route('/')
def index():
    pass

if __name__ == '__main__':
    app.run(debug=True)

