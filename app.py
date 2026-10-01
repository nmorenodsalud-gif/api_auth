from flask import Flask

app = Flask(__name__)

@app.get("/")
def inicio():
    return {"mensaje": "Hola, mi primera API funciona"}

if __name__ == "__main__":
    app.run(port=5000, debug=True)