from flask import Flask
from flask import render_template

app = Flask(__name__)

table = [(0, 'frank', 28, '224400'), (1, 'jack', 35, ''), (2, 'lucy', 22, '')]


@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('fortest.html', table = table )

if __name__=="__main__":
    app.run("0.0.0.0", 5000, True)
