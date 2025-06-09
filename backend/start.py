import os
import sys
import uvicorn
from pathlib import Path

def main():
    # Add the parent directory to Python path so we can import python_control
    project_root = Path(__file__).parent.parent
    sys.path.append(str(project_root))
    
    # Start the FastAPI server
    PORT = 9000
    print("Starting Arduino LED Control API server...")
    print(f"API documentation will be available at http://localhost:{PORT}/docs")
    print(f"MCP server will be available at http://localhost:{PORT}/mcp")    
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)

if __name__ == "__main__":
    main()
