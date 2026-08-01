"""
discord_bot_utils.py
--------------------
Helper functions for discord_bot.py command handlers.
"""

import asyncio
import json
from pathlib import Path

from utils.format_status_report import format_status_report

from utils.format_decisions import format_decisions

from utils.format_log_entries import format_log_entries

async def run_subprocess(ctx, *args, success_msg, failure_header):
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode == 0:
        await ctx.send(success_msg)
    else:
        await ctx.send(f"{failure_header} with exit code {process.returncode}.\nError:\n```\n{stderr.decode(errors='replace')[-1000:]}\n```")

from utils.format_command_output import format_command_output
