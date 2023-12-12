from metagpt.roles import Role
from metagpt.actions import GeneratePostImage, WriteTasks
from metagpt.schema import Message
from metagpt.logs import logger


class ContentGenerator(Role):
    def __init__(
        self,
        name: str = "Mauro",
        profile: str = "ContentGenerator",
        **kwargs,
    ):
        super().__init__(name, profile, **kwargs)
        self._init_actions([GeneratePostImage])
        self._watch([WriteTasks])

    # async def _act(self) -> Message:
    #     logger.info(f"{self._setting}: ready to {self._rc.todo}")
    #     todo = self._rc.todo

    #     msg = self._rc.memory.get_by_actions([WriteTasks])
    #     print(msg)

    #     code_text = await todo.run(msg.content)
    #     msg = Message(content=code_text, role=self.profile, cause_by=type(todo))

    #     return msg
