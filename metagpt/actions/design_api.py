#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 19:26
@Author  : alexanderwu
@File    : design_api.py
"""
import shutil
from pathlib import Path
from typing import List

from metagpt.actions import Action, ActionOutput
from metagpt.const import WORKSPACE_ROOT
from metagpt.logs import logger
from metagpt.utils.common import CodeParser
from metagpt.utils.mermaid import mermaid_to_file
from metagpt.actions.search_and_summarize import SearchAndSummarize

PROMPT_TEMPLATE = """
# Context
{context}

## Search Information
{search_information}

## Format example
{format_example}
-----
Role: As the Marketing Strategist Agent in an autonomous digital marketing agency, your primary role is to develop the overarching strategy for marketing campaigns, guided by inputs from the Account Executive Agent. You are responsible for crafting strategies that not only align with the client's goals and budget but also effectively leverage various marketing channels and insights derived from market research and consumer behavior analysis.
Requirement: Fill in the following missing information based on the context.
Max Output: 8192 chars or 2048 tokens. Try to use them up.
Attention: Use '##' to split sections, not '#', and '## <SECTION_NAME>'

## Strategy Formulation: Provide as Plain text. Develop comprehensive marketing strategies that align with the client's objectives, as communicated by the Account Executive. This includes selecting appropriate marketing channels, defining target audiences, and setting campaign goals.

## Market Research and Consumer Insights: Provided as a list of markdown bullet points, up to 10 market and consumer insights. Conduct in-depth market research and analyze consumer behavior to inform strategy development. Stay updated with market trends, competitor activities, and emerging marketing techniques.

## Budget Allocation: Provided as a list of markdown bullet points, up to 5 budget allocation. Allocate the client's budget across various marketing channels and activities, ensuring that the budget is spent efficiently and effectively.

## Creation of Detailed Campaign Briefs: Provide as Plain Text. Produce comprehensive briefs outlining the strategy, objectives, target audience, key messages, and specific tactics for each aspect of the campaign. These briefs should provide clear, actionable guidance for specialized agents, ensuring efficient execution of the strategy. 

## Anything UNCLEAR: Provide as Plain text. Make clear here.

"""
FORMAT_EXAMPLE = """
---
## Strategy Formulation
We will ...

## Market Research and Consumer Insights
- Insight 1
- Insight 2
- Insight 3

## Budget Allocation
- Instagram: 30%,
- Facebook: 30%,

## Creation of Detailed Campaign Briefs
We will ...

## Anything UNCLEAR
The requirement is clear to me.
---
"""
OUTPUT_MAPPING = {
    "Strategy Formulation": (str, ...),
    "Market Research and Consumer Insights": (str, ...),
    "Budget Allocation": (str, ...),
    "Creation of Detailed Campaign Briefs": (str, ...),
    "Anything UNCLEAR": (str, ...),
}


class WriteDesign(Action):
    def __init__(self, name, context=None, llm=None):
        super().__init__(name, context, llm)
        self.desc = "You are responsible for crafting strategies that not only align with the client's goals and budget but also effectively leverage various marketing channels and insights derived from market research and consumer behavior analysis"

    def recreate_workspace(self, workspace: Path):
        try:
            shutil.rmtree(workspace)
        except FileNotFoundError:
            pass  # 文件夹不存在，但我们不在意
        workspace.mkdir(parents=True, exist_ok=True)

    def _save_prd(self, docs_path, resources_path, prd):
        prd_file = docs_path / "prd.md"
        quadrant_chart = CodeParser.parse_code(
            block="Competitive Quadrant Chart", text=prd
        )
        mermaid_to_file(quadrant_chart, resources_path / "competitive_analysis")
        # logger.info(f"Saving PRD to {prd_file}")
        # prd_file.write_text(prd)

    def _save_system_design(self, docs_path, resources_path, content):
        data_api_design = CodeParser.parse_code(
            block="Data structures and interface definitions", text=content
        )
        seq_flow = CodeParser.parse_code(block="Program call flow", text=content)
        mermaid_to_file(data_api_design, resources_path / "data_api_design")
        mermaid_to_file(seq_flow, resources_path / "seq_flow")
        system_design_file = docs_path / "system_design.md"
        logger.info(f"Saving System Designs to {system_design_file}")
        system_design_file.write_text(content)

    def _save(self, context, system_design):
        if isinstance(system_design, ActionOutput):
            content = system_design.content
            ws_name = CodeParser.parse_str(block="Python package name", text=content)
        else:
            content = system_design
            ws_name = CodeParser.parse_str(
                block="Python package name", text=system_design
            )
        workspace = WORKSPACE_ROOT / ws_name
        self.recreate_workspace(workspace)
        docs_path = workspace / "docs"
        resources_path = workspace / "resources"
        docs_path.mkdir(parents=True, exist_ok=True)
        resources_path.mkdir(parents=True, exist_ok=True)
        self._save_prd(docs_path, resources_path, context[-1].content)
        self._save_system_design(docs_path, resources_path, content)

    async def run(self, context):
        sas = SearchAndSummarize()
        # rsp = await sas.run(context=requirements, system_text=SEARCH_AND_SUMMARIZE_SYSTEM_EN_US)
        rsp = ""
        info = f"### Search Results\n{sas.result}\n\n### Search Summary\n{rsp}"
        if sas.result:
            logger.info(sas.result)
            logger.info(rsp)
        prompt = PROMPT_TEMPLATE.format(
            context=context, search_information=info, format_example=FORMAT_EXAMPLE
        )
        # system_design = await self._aask(prompt)
        system_design = await self._aask_v1(prompt, "system_design", OUTPUT_MAPPING)
        # docs_path = WORKSPACE_ROOT / "docs"
        # resources_path = WORKSPACE_ROOT / "resources"
        # docs_path.mkdir(parents=True, exist_ok=True)
        # resources_path.mkdir(parents=True, exist_ok=True)
        # # self._save_prd(docs_path, resources_path, context[-1].content)
        file_path = WORKSPACE_ROOT / "strategy.md"
        file_path.write_text(system_design.content)
        # self._save(context, system_design)
        return system_design
