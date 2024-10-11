from src.endpoints import app

if __name__ == '__main__':
    port = 3000
    host = "0.0.0.0"
    app.run(port=port, host=host)

