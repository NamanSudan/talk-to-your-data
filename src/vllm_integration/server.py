
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from vllm import AsyncLLMEngine
from vllm.engine.arg_utils import AsyncEngineArgs
import uvicorn
from fastapi import FastAPI
from src.vllm_integration.config import VLLM_CONFIG

app = FastAPI()

# Initialize engine once at startup
engine_args = AsyncEngineArgs(
    model=VLLM_CONFIG["model_name"],
    enable_lora=VLLM_CONFIG["enable_lora"],
    device="cpu",
    dtype="float32"
)
engine = AsyncLLMEngine.from_engine_args(engine_args)

@app.post("/generate")
async def generate(request: dict):
    sampling_params = {
        "temperature": request.get("temperature", 0.1),
        "max_tokens": request.get("max_tokens", VLLM_CONFIG["max_tokens"]),
        "stop": request.get("stop", [";", "\n"])
    }
    prompt = request.get("prompt")
    
    result = await engine.generate(prompt, sampling_params)
    return {"text": result.outputs[0].text}

def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_server()
