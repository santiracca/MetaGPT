#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : architect.py
"""

from metagpt.actions import WriteDesign, WritePRD
from metagpt.roles import Role


class CampaignStrategist(Role):
    """CampaignStrategist: Listen to PRD, responsible for designing a marketing campaign. """
    def __init__(self, name="Manu", profile="Campaign Strategist", goal="Develop the overarching strategy for marketing campaigns, guided by inputs from the PRD",
                 constraints="Align with the client's goals and budget but also effectively leverage various marketing channels and insights derived from market research and consumer behavior analysis."):
        super().__init__(name, profile, goal, constraints)
        self._init_actions([WriteDesign])
        self._watch({WritePRD})
