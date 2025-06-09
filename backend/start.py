import os
import sys
import uvicorn
from pathlib import Path

def main():
    # Add the parent directory to Python path so we can import python_control
    project_root = Path(__file__).parent.parent
    sys.path.append(str(project_root))
    
    # Start the FastAPI server
    print("Starting Arduino LED Control API server...")
    print("API documentation will be available at http://localhost:9000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)

if __name__ == "__main__":
    main()
