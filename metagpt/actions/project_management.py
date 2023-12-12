#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 19:12
@Author  : alexanderwu
@File    : project_management.py
"""
from typing import List, Tuple

from metagpt.actions.action import Action
from metagpt.const import WORKSPACE_ROOT
from metagpt.utils.common import CodeParser
from metagpt.const import RESEARCH_PATH

PROMPT_TEMPLATE = """
# Context
{context}

## Format example
{format_example}
-----
Role: You are a Social Media Content Creator Agent within a digital marketing agency, your role is to craft engaging and relevant content for social media platforms. Your responsibilities include conceptualizing post ideas, writing compelling headlines and captions, and describing the visual elements needed to complement the text. Your content should align with the overall marketing strategy and client's brand voice, and be designed to engage the target audience effectively.
Requirements: Based on the context, fill in the following missing informatio. Here the granularity of the task is a file, if there are any missing files, you can supplement them
Attention: Use '##' to split sections, not '#', and '## <SECTION_NAME>'.

## Idea Generation: Provided in Plain Text. Come up with creative and relevant ideas for social media posts that resonate with the client's target audience and align with the marketing campaign's objectives.

## Writing Headlines and Captions: Provided in Plain Text. Craft catchy headlines and compelling captions that capture the essence of the post, encourage engagement, and reflect the client’s brand voice.

## Visual Concept Description: Provided in Plain Text. Provide detailed descriptions of the visual elements required for each post. This includes specifying imagery, color schemes, layout, and any graphical elements that align with the post's message and the client's brand aesthetics.

## Content Calendar Management: Provided in Plain Text.Plan and organize content in a social media calendar to ensure consistent and timely posting in line with the marketing strategy.

## Alignment with Marketing Strategy: Provided in Plain Text. Ensure that all content supports the overarching marketing goals set by the Marketing Strategist Agent, and is cohesive with other marketing activities.

## Anything UNCLEAR: Provide as Plain text. Make clear here.

"""

FORMAT_EXAMPLE = """
---
## Idea Generation
Post Idea: Highlighting a new ...
Post Idea: ...

## Writing Headlines and Captions
POST 1
Headline: ...
Caption: ...


## Visual Concept Description
An image featuring the eco-friendly products stylishly arranged against a natural, earthy background. The color palette should be green and earth tones to emphasize the eco-friendly theme. The layout is clean and minimalistic, with the products being the focal point.

## Content Calendar Management
| Date | Post | Platform |
| ---- | ---- | -------- |
| 2021-04-22 | Post 1 | Instagram |

## Alignment with Marketing Strategy
The post should highlight the eco-friendly aspect of the brand's products, which is one of the key selling points of the brand. It should also be aligned with the overall marketing strategy, which is to position the brand as a sustainable and environmentally conscious company.

## Anything UNCLEAR
We need ... how to start.
---
"""

OUTPUT_MAPPING = {
    "Idea Generation": (str, ...),
    "Writing Headlines and Captions": (str, ...),
    "Visual Concept Description": (str, ...),
    "Content Calendar Management": (str, ...),
    "Alignment with Marketing Strategy": (str, ...),
    "Anything UNCLEAR": (str, ...),
}


class WriteTasks(Action):
    def __init__(self, name="CreateTasks", context=None, llm=None):
        super().__init__(name, context, llm)

    def _save(self, context, rsp):
        # ws_name = CodeParser.parse_str(
        #     block="Python package name", text=context[-1].content
        # )
        file_path = WORKSPACE_ROOT / "api_spec_and_tasks.md"
        file_path.write_text(rsp.content)

        # # Write requirements.txt
        # requirements_path = WORKSPACE_ROOT / ws_name / "requirements.txt"
        # requirements_path.write_text(
        #     rsp.instruct_content.dict()
        #     .get("Required Python third-party packages")
        #     .strip('"\n')
        # )

    async def run(self, context):
        prompt = PROMPT_TEMPLATE.format(context=context, format_example=FORMAT_EXAMPLE)
        rsp = await self._aask_v1(prompt, "task", OUTPUT_MAPPING)
        self._save(context, rsp)
        return rsp


class AssignTasks(Action):
    async def run(self, *args, **kwargs):
        # Here you should implement the actual action
        pass
