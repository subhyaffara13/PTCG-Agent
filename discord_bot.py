"""
discord_bot.py

A background daemon that bridges Discord to the ptcg-agent workspace.
Allows monitoring evaluation scores, training progress, and decisions remotely.
"""

import os
import sys
import asyncio
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv

from discord_bot_utils import format_status_report, format_decisions, format_log_entries, run_subprocess, format_command_output

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("PTCG Discord Bridge is online and listening!")

@bot.command(name="status")
async def status(ctx):
    report_file = Path("logs/eval_report.json")
    if not report_file.exists():
        await ctx.send("No evaluation report found yet. Train the model first using !train.")
        return
    try:
        await ctx.send(format_status_report(report_file))
    except Exception as e:
        await ctx.send(f"Error reading status report: {e}")

@bot.command(name="decisions")
async def decisions(ctx):
    dec_file = Path("decisions.md")
    if not dec_file.exists():
        await ctx.send("No decision log found.")
        return
    try:
        await ctx.send(format_decisions(dec_file))
    except Exception as e:
        await ctx.send(f"Error reading decision log: {e}")

@bot.command(name="log")
async def log(ctx, component: str = "prize_mapper"):
    path_map = {"prize_mapper": "logs/prize_mapper_reasoning.json", "opponent_model": "logs/opponent_model_reasoning.json"}
    if component not in path_map:
        await ctx.send("Invalid component. Choose 'prize_mapper' or 'opponent_model'.")
        return
    path = Path(path_map[component])
    if not path.exists():
        await ctx.send(f"No reasoning logs found for {component}.")
        return
    try:
        await ctx.send(format_log_entries(component, path))
    except Exception as e:
        await ctx.send(f"Error reading logs: {e}")

@bot.command(name="train")
async def train(ctx, iterations: int = 10):
    await ctx.send(f"🚀 Starting {iterations} guided training iterations in the background...")
    try:
        await run_subprocess(ctx, sys.executable, "run_guided_iterations.py", str(iterations),
                             success_msg=f"✅ Guided training of {iterations} iterations completed successfully!",
                             failure_header="❌ Guided training failed")
    except Exception as e:
        await ctx.send(f"Failed to launch training: {e}")

@bot.command(name="run_cmd")
async def run_cmd(ctx, *, command: str):
    await ctx.send(f"💻 Running command: `{command}`...")
    try:
        process = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        await ctx.send(format_command_output(process.returncode, stdout, stderr))
    except Exception as e:
        await ctx.send(f"Error executing command: {e}")

if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_TOKEN is missing in the .env file.")
    else:
        bot.run(TOKEN)
