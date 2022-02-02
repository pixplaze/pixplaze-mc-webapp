from app import app


@app.route('/')
def api():
    return {'Hello': 'world!'}
