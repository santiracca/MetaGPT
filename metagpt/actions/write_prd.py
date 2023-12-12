"""
@Time    : 2023/5/11 17:45
@Author  : alexanderwu
@File    : write_prd.py
"""
from typing import List, Tuple

from metagpt.actions import Action, ActionOutput
from metagpt.actions.search_and_summarize import SearchAndSummarize
from metagpt.logs import logger
from metagpt.const import WORKSPACE_ROOT
from metagpt.utils.common import CodeParser
from metagpt.utils.mermaid import mermaid_to_file

PROMPT_TEMPLATE = """
# Context
## Original Requirements
{requirements}

## Search Information
{search_information}

## mermaid quadrantChart code syntax example. DONT USE QUOTE IN CODE DUE TO INVALID SYNTAX. Replace the <Campain X> with REAL COMPETITOR NAME
```mermaid
quadrantChart
    title Reach and engagement of campaigns
    x-axis Low Reach --> High Reach
    y-axis Low Engagement --> High Engagement
    quadrant-1 We should expand
    quadrant-2 Need to promote
    quadrant-3 Re-evaluate
    quadrant-4 May be improved
    "Campaign: A": [0.3, 0.6]
    "Campaign B": [0.45, 0.23]
    "Campaign C": [0.57, 0.69]
    "Campaign D": [0.78, 0.34]
    "Campaign E": [0.40, 0.34]
    "Campaign F": [0.35, 0.78]
    "Our Target Product": [0.5, 0.6]
```

## Format example
{format_example}
-----
Role: As an Account Executive Agent in an autonomous digital marketing agency, your primary role is to act as the main point of contact between the client and the agency. Your responsibilities encompass understanding and translating client requirements into actionable marketing strategies, coordinating with specialized agents, and ensuring the successful execution and monitoring of marketing campaigns. Your aim is to provide seamless, effective communication and project management while aligning all marketing activities with the client's goals.
Requirements: According to the context, fill in the following missing information. If the requirements are unclear, ensure minimum viability and avoid excessive design
ATTENTION: Use '##' to SPLIT SECTIONS, not '#'. AND '## <SECTION_NAME>'. Output carefully referenced "Format example" in format.

## Original Requirements: Provide as Plain text, place the polished complete original requirements here

## Campaign Goals: Provided as list of markdown bulletpoints, up to 3 clear, orthogonal campaign goals. If the requirement itself is simple, the goal should also be simple

## Target Market Call-to-Action goals: Provided as markdown bullet points, up to 5 scenario-based call-to-action, If the requirement itself is simple, the call-to-action should also be less

## Competitive Analysis: Provided list of markdown bulletpoints, up to 7 competitive product analyses, consider as similar competitors as possible

## Competitive Quadrant Chart: Use mermaid quadrantChart code syntax. up to 14 competitive products. Distribute these competitor scores evenly between 0 and 1, trying to conform to a normal distribution centered around 0.5 as much as possible.

## Requirement Analysis: Provide as Plain text. Be simple. LESS IS MORE. Make your requirements less dumb. Delete the parts unnessasery.

## Requirement Pool: Provided as list of markdown bulletpoints, the parameters are requirement description, priority(P0/P1/P2), respectively, comply with PEP standards; no more than 5 requirements and consider to make its difficulty lower

## Anything UNCLEAR: Provide as Plain text. Make clear here.

## Additional Information Required: Provided as markdown bullet points, up to 5 pieces of additional information needed from the client to help you deliver better results. ONLY IF YOU NEED MORE INFORMATION.
"""
FORMAT_EXAMPLE = """
---
## Original Requirements
The boss ... 

## Campaign Goals

-  Create a ...
-  Increase ...

## Target Market Call-to-Action goals

- I want my customers to ...
- I want my customers to ...

## Competitive Analysis

- Competitor: ...

## Competitive Quadrant Chart
```mermaid
quadrantChart
    title Reach and engagement of campaigns
    ...
    "Our Target Campaign": [0.6, 0.7]
```

## Requirement Analysis
The product should be a ...

## Requirement Pool
| Requirement | Priority | 
| -------- | -------- |
| Campaign requirement   | P0  | 
| Campaign requirement   | P1  |



## Anything UNCLEAR
There are no unclear points.

## Additional Information Required.
- I want to know ...
---
"""
OUTPUT_MAPPING = {
    "Original Requirements": (str, ...),
    "Campaign Goals": (str, ...),
    "Target Market Call-to-Action goals": (str, ...),
    "Competitive Analysis": (str, ...),
    "Competitive Quadrant Chart": (str, ...),
    "Requirement Analysis": (str, ...),
    "Requirement Pool": (str, ...),
    "Anything UNCLEAR": (str, ...),
    "Additional Information Required": (str, ...),
}


class WritePRD(Action):
    def __init__(self, name="", context=None, llm=None):
        super().__init__(name, context, llm)

    async def run(self, requirements, *args, **kwargs) -> ActionOutput:
        sas = SearchAndSummarize()
        # rsp = await sas.run(context=requirements, system_text=SEARCH_AND_SUMMARIZE_SYSTEM_EN_US)
        rsp = ""
        info = f"### Search Results\n{sas.result}\n\n### Search Summary\n{rsp}"
        if sas.result:
            logger.info(sas.result)
            logger.info(rsp)

        prompt = PROMPT_TEMPLATE.format(
            requirements=requirements,
            search_information=info,
            format_example=FORMAT_EXAMPLE,
        )
        logger.debug(prompt)
        prd = await self._aask_v1(prompt, "prd", OUTPUT_MAPPING)
        file_path = WORKSPACE_ROOT / "prd.md"
        file_path.write_text(prd.content)
        quadrant_chart = CodeParser.parse_code(
            block="Competitive Quadrant Chart", text=prd.content
        )
        mermaid_to_file(quadrant_chart, WORKSPACE_ROOT / "competitive_analysis")
        return prd
