from flask import Flask, render_template

app = Flask(__name__)

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

#Rota codificar
@app.route('/codificar')
def codificar():
    return render_template('codificar.html')
