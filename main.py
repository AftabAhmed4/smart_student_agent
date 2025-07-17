import os
import chainlit as cl
from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig,
    Agent,
    Runner
)

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
gemini_api_key =os.getenv("GEMINI_API_KEY")


# step # 1 set up provider
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# setup # 2 modal
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", 
    openai_client=provider
)



# step # 3 configuration 
config = RunConfig(
    model_provider= provider,
    model=model,
    tracing_disabled=True
)


# step # 4 Agent
agent = Agent(
    name="smart student agent",
    instructions="You are smart full agent"

)

 

@cl.on_message
async def main(message :cl.Message):
    
    result = Runner.run_sync(
        agent,
        input=message.content,
        run_config=config,

    )
    await cl.Message(result.final_output).send()