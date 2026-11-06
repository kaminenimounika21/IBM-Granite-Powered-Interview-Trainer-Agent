"""
IBM Granite Interview Trainer Agent - Application Launcher
Executes the FastAPI server with IBM Carbon theme and live watsonx / Docling engines.
"""

import uvicorn
from app.config import settings

def main():
    print("=" * 70)
    print("IBM GRANITE-POWERED INTERVIEW TRAINER AGENT")
    print(f"Version: {settings.APP_VERSION}")
    print(f"Foundation Model: {settings.WATSONX_MODEL_ID}")
    print(f"Document Intelligence: IBM Docling Core 2.106.0")
    print(f"Server starting on http://{settings.HOST}:{settings.PORT}")
    print("=" * 70)
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
