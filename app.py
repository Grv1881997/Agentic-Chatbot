from dotenv import load_dotenv

load_dotenv()

from src.langgraphagenticai.main import load_langgraph_agenticai_app

if __name__=="__main__":
    load_langgraph_agenticai_app()