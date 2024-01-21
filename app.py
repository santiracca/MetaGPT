#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import platform
import fire
from flask import Flask, request, Response, send_file
from threading import Thread
import zipfile
import os


app = Flask(__name__)


@app.route("/agentC", methods=["POST"])
def agentC():
    data = request.get_json()
    idea = data.get("idea")
    investment = data.get("investment", 3.0)
    n_round = data.get("n_round", 5)
    code_review = data.get("code_review", False)
    run_tests = data.get("run_tests", False)

    def run_project():
        if platform.system() == "Windows":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        yield "Starting agentC...\n"
        Thread(
            target=asyncio.run,
            args=(startup(idea, investment, n_round, code_review, run_tests),),
        ).start()
        yield "Done.\n"

    return Response(run_project(), mimetype="text/plain")


@app.route("/files", methods=["GET"])
def files():
    # Create a zip file
    with zipfile.ZipFile("files.zip", "w") as zipf:
        for file in os.listdir("./workspace"):
            zipf.write(f"./workspace/{file}")

    # Send the zip file
    return send_file("files.zip", as_attachment=True)


from metagpt.roles import (
    CampaignStrategist,
    Engineer,
    AccountExecutive,
    ContentCreator,
    QaEngineer,
    ContentGenerator,
)
from metagpt.marketing_agency import MarketingAgency


async def startup(
    idea: str,
    investment: float = 3.0,
    n_round: int = 5,
    code_review: bool = False,
    run_tests: bool = False,
):
    """Run a digital marketing agency. Be a boss."""
    company = MarketingAgency()
    company.hire(
        [
            AccountExecutive(),
            CampaignStrategist(),
            ContentCreator(),
            # ContentGenerator(),
        ]
    )
    company.invest(investment)
    company.start_project(idea)
    await company.run(n_round=n_round)


def main(
    idea: str,
    investment: float = 3.0,
    n_round: int = 5,
    code_review: bool = False,
    run_tests: bool = False,
):
    """
    We are a digital marketing agency comprised of AI. By investing in us, you are empowering a future filled with limitless possibilities.
    :param idea: Your innovative idea, such as "Creating a new marketing campaign."
    :param investment: As an investor, you have the opportunity to contribute a certain dollar amount to this AI company.
    :param n_round:
    :param code_review: Whether to use code review.
    :return:
    """
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(startup(idea, investment, n_round, code_review, run_tests))


if __name__ == "__main__":
    app.run(debug=True)
