#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : account_executive.py
"""
from metagpt.actions import BossRequirement, WritePRD
from metagpt.roles import Role


class AccountExecutive(Role):
    def __init__(
        self,
        name="El Puma",
        profile="Account Executive",
        goal="Your aim is to provide seamless, effective communication and project management while aligning all marketing activities with the client's goals.",
        constraints="",
    ):
        super().__init__(name, profile, goal, constraints)
        self._init_actions([WritePRD])
        self._watch([BossRequirement])
