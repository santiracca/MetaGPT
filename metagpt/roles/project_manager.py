#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 15:04
@Author  : alexanderwu
@File    : project_manager.py
"""
from metagpt.actions import WriteDesign, WriteTasks, BossRequirement
from metagpt.roles import Role


class ContentCreator(Role):
    def __init__(
        self,
        name="Emilin",
        profile="Social Media Content Creator",
        goal="Craft engaging and relevant content for social media platforms",
        constraints="create content that not only captures the audience's attention but also fosters a connection with the brand, driving engagement and aligning with the overall marketing goals. Your content should be fresh, relevant, and tailored to the specific nuances of the social media platforms being targeted.",
    ):
        super().__init__(name, profile, goal, constraints)
        self._init_actions([WriteTasks])
        self._watch([WriteDesign])
