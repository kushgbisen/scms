from main import app

# Vercel serverless function entry point
def handler(request):
    return app(request.environ, start_response=lambda status, headers: None)

# Required for Vercel
app.debug = False
if __name__ == "__main__":
    app.run()
