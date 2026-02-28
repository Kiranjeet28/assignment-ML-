import os
# Suppress "PyTorch was not found" warning — we use InferenceClient (API-only)
os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

from functools import lru_cache
from typing import Any, List, Optional

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from langchain_core.language_models.llms import LLM
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

_CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "titanic.csv")

SYSTEM_PROMPT = (
    "You are a data analyst working strictly with the Titanic dataset. "
    "Only use the dataframe provided. Never access system files or external data. "
    "If the question requires a visualization, clearly state that a plot is required. "
    "Be concise and accurate."
)


class QwenInferenceLLM(LLM):
    """
    LangChain-compatible LLM wrapper around HuggingFace InferenceClient
    using the Together AI provider. No local model or GPU required.
    """

    model_name: str = MODEL_NAME
    hf_token: str = ""
    max_new_tokens: int = 512
    temperature: float = 0.1

    @property
    def _llm_type(self) -> str:
        return "qwen-inference-client"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> str:
        client = InferenceClient(
            provider="together",
            api_key=self.hf_token,
        )
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt},
            ],
            max_tokens=self.max_new_tokens,
            temperature=self.temperature,
            stop=stop,
        )
        return response.choices[0].message.content or ""


def get_llm() -> QwenInferenceLLM:
    return QwenInferenceLLM(
        model_name=MODEL_NAME,
        hf_token=HF_TOKEN or "",
        max_new_tokens=512,
        temperature=0.1,
    )


@lru_cache(maxsize=1)
def get_agent():
    """
    Build and cache the pandas dataframe agent once per process.
    Uses Together AI's hosted Qwen2.5-7B-Instruct via InferenceClient.
    """
    df = pd.read_csv(_CSV_PATH)
    llm = get_llm()

    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        # FIX: "openai-tools" requires OpenAI's function-calling protocol.
        # Use "zero-shot-react-description" which works with any LLM.
        agent_type="zero-shot-react-description",
        allow_dangerous_code=True,
        prefix=SYSTEM_PROMPT,
    )
    return agent