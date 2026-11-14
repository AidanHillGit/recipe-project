# 1. Import the FastAPI class from the fastapi package
from fastapi import FastAPI

# 2. Create an instance of FastAPI and store it in a variable named app
app = FastAPI()

# 3. Define GET /health:
#    - a decorator on the app that registers a GET route for "/health"
#    - a function under it (name it something descriptive)
#    - the function returns a dictionary: status → "ok"

@app.get('/health')
async def health_check():
    return {"status": "ok"}