# Initialize command: uvicorn src.arturito-api.app:app
import os
import yaml

from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

from arq import create_pool
from arq.connections import RedisSettings

load_dotenv()

REDIS_PARAMS = {
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": os.getenv("REDIS_PORT", 6379),
    "password": os.getenv("REDIS_PASSWORD"),
}

class AgentConfig(BaseModel):
    name: str = Field(description="Name of the agent.")
    description: str = Field(description="Description of the agent's purpose and behavior.")
    owner: str = Field(description="Owner of the agent.")
    model: str = Field(description="LLM to be used by the agent.")

# 1. Initialize the FastAPI app
app = FastAPI()

class ChatRequest(BaseModel):
    messages: list
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 100
    stream: Optional[bool] = False

async def create_job(task_name: str, **kwargs):
    redis = await create_pool(
        RedisSettings(**REDIS_PARAMS)
    )

    job = await redis.enqueue_job(task_name, **kwargs)
    result = await job.result(timeout=int(os.getenv("ARQ_JOB_TIMEOUT", 30)))

    return result

@app.post("/agents")
async def create_agent(config: dict):
    result = await create_job("create_agent", config=config)
    return {result}

@app.post("/agents/search")
async def search_agents():
    pass

@app.post("/agents/count")
async def count_agents():
    pass

@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    pass

@app.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    pass

@app.post("/sessions")
async def call_agent(request: ChatRequest):
    pass

@app.get("/sessions/{session_id}")
async def call_agent(session_id: str, request: ChatRequest):
    pass

@app.get("/sessions/{session_id}/state")
async def call_agent(session_id: str, request: ChatRequest):
    pass    

@app.post("/sessions/{session_id}/runs")
async def call_agent(session_id: str, request: ChatRequest):
    pass   

@app.post("/sessions/{session_id}/runs/stream")
async def call_agent(session_id: str, request: ChatRequest):
    pass   

@app.get("/sessions/{session_id}/runs/{run_id}")
async def call_agent(session_id: str, request: ChatRequest):
    pass   

@app.post("/sessions/{session_id}/runs/{run_id}/cancel")
async def call_agent(session_id: str, request: ChatRequest):
    pass   
