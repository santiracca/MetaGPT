#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : __init__.py
"""

from metagpt.roles.role import Role
from metagpt.roles.architect import CampaignStrategist
from metagpt.roles.project_manager import ContentCreator
from metagpt.roles.account_executive import AccountExecutive
from metagpt.roles.engineer import Engineer
from metagpt.roles.qa_engineer import QaEngineer
from metagpt.roles.seacher import Searcher
from metagpt.roles.sales import Sales
from metagpt.roles.customer_service import CustomerService
from metagpt.roles.post_generator import ContentGenerator


__all__ = [
    "Role",
    "ContentGenerator",
    "CampaignStrategist",
    "ContentCreator",
    "AccountExecutive",
    "Engineer",
    "QaEngineer",
    "Searcher",
    "Sales",
    "CustomerService",
]
