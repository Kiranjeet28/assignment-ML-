# Render FastAPI Backend Deployment

## 1. Create requirements.txt (if not already present)
# (You already have this file, but ensure it includes these)
# fastapi
# uvicorn
# (plus any other dependencies your backend needs)

## 2. Create a render.yaml (optional, for Infrastructure as Code)

## 3. Create a start command for Render

# In your backend directory, create a file named 'render_start.sh':

#!/bin/bash
uvicorn backend.main:app --host 0.0.0.0 --port 10000

# Make it executable (locally):
# chmod +x backend/render_start.sh

## 4. Deploy Steps
# 1. Push your code to GitHub.
# 2. Go to https://dashboard.render.com/
# 3. Click 'New Web Service'.
# 4. Connect your GitHub repo.
# 5. Set the root directory to your project root.
# 6. Set the build command to:
#    pip install -r requirements.txt
# 7. Set the start command to:
#    bash backend/render_start.sh
# 8. Set the environment to Python 3.9+.
# 9. Set the port to 10000 (or your preferred port).
# 10. Deploy.

# After deployment, update API_URL in your Streamlit app to point to the Render backend URL.
