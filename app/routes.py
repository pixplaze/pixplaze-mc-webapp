from app import app
@app.route('/')
def api():
    return {'gnida': 'dada'}