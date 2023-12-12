from metagpt.actions import Action
from metagpt.config import CONFIG as config
from metagpt.logs import logger

# openai.api_key = config.openai_api_key

# client = openai.OpenAI()

# # client.images.generate(
# #   model="dall-e-3",
# #   prompt="A cute baby sea otter",
# #   n=1,
# #   size="1024x1024"
# # )


class GeneratePostImage(Action):
    PROMPT_TEMPLATE = """
    Write a python function that can {instruction} and provide two runnnable test cases.
    Return ```python your_code_here ``` with NO other texts,
    your code:
    """

    def __init__(self, name="GeneratePostImage", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, instruction):
        for message in instruction:
            logger.info(f"{message.content}")
            image = self.llm.generate_image(message.content)
            logger.info(f"image: {image}")

    @staticmethod
    def parse_code(rsp):
        pattern = r"```python(.*)```"
        match = re.search(pattern, rsp, re.DOTALL)
        code_text = match.group(1) if match else rsp
        return code_text
