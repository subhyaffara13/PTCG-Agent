"""
discord_bot.py

A background daemon that bridges Discord to the ptcg-agent workspace.
Allows monitoring evaluation scores, training progress, and decisions remotely.
"""

import os
import json
from pathlib import Path
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup bot intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("PTCG Discord Bridge is online and listening!")

@bot.command(name="status")
async def status(ctx):
    """Reports the current status of the training factory and latest baseline scores."""
    report_file = Path("logs/eval_report.json")
    if not report_file.exists():
        await ctx.send("No evaluation report found yet. Train the model first using !train.")
        return

    try:
        report = json.loads(report_file.read_text(encoding="utf-8"))
        iter_id = report.get("iteration", "unknown")
        raw_scores = report.get("raw_scores", {})
        version_scores = report.get("version_scores", {})
        best_ver = version_scores.get("best_version", "unknown")
        best_score = version_scores.get(best_ver, 0.0)

        msg = (
            f"**🏆 PTCG Agent Current Status**\n"
            f"• **Current Iteration:** {iter_id}\n"
            f"• **Peak Baseline Local Score:** `{best_score}` (Version: `{best_ver}`)\n"
            f"• **Reasoning Test Score:** `{raw_scores.get('reasoning_test', 0.0)}`\n"
            f"• **Deck Test Score:** `{raw_scores.get('deck_test', 0.0)}`\n"
            f"• **Variance Baseline Score:** `{raw_scores.get('variance_baseline', 0.0)}`"
        )
        await ctx.send(msg)
    except Exception as e:
        await ctx.send(f"Error reading status report: {e}")

@bot.command(name="decisions")
async def decisions(ctx):
    """Retrieves the latest decision log entries from decisions.md."""
    dec_file = Path("decisions.md")
    if not dec_file.exists():
        await ctx.send("No decision log found.")
        return

    try:
        content = dec_file.read_text(encoding="utf-8")
        # Extract the last few entries
        entries = content.split("## Iteration ")
        if len(entries) <= 1:
            await ctx.send("Decision log is empty.")
            return
            
        last_entries = entries[-3:] # Get last 3 iterations
        result_text = "**📝 Recent Decision Log Entries:**\n"
        for item in last_entries:
            result_text += f"\n*Iteration {item.strip()[:1000]}*\n"
            
        if len(result_text) > 2000:
            result_text = result_text[:1990] + "\n...(truncated)"
            
        await ctx.send(result_text)
    except Exception as e:
        await ctx.send(f"Error reading decision log: {e}")

@bot.command(name="log")
async def log(ctx, component: str = "prize_mapper"):
    """Reads the latest lines from the requested reasoning logs (component = prize_mapper or opponent_model)."""
    if component == "prize_mapper":
        path = Path("logs/prize_mapper_reasoning.json")
    elif component == "opponent_model":
        path = Path("logs/opponent_model_reasoning.json")
    else:
        await ctx.send("Invalid component. Choose 'prize_mapper' or 'opponent_model'.")
        return

    if not path.exists():
        await ctx.send(f"No reasoning logs found for {component}.")
        return

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not data:
            await ctx.send("Logs are empty.")
            return

        latest = data[-3:]  # Get last 3 entries
        msg = f"**📊 Latest Heuristic Reasoning for `{component}`:**\n"
        for i, entry in enumerate(latest):
            msg += f"\n**Turn {entry.get('turn')} ({entry.get('perspective')}):**\n```json\n"
            cleaned_entry = {k: v for k, v in entry.items() if k not in ("turn", "perspective")}
            msg += json.dumps(cleaned_entry, indent=2)[:500]
            msg += "\n```"
        await ctx.send(msg)
    except Exception as e:
        await ctx.send(f"Error reading logs: {e}")

@bot.command(name="train")
async def train(ctx, iterations: int = 10):
    """Triggers guided training iterations in the background."""
    await ctx.send(f"🚀 Starting {iterations} guided training iterations in the background...")
    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable, "run_guided_iterations.py", str(iterations),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await ctx.send(f"Task spawned with PID: `{process.pid}`. I will report back when finished!")
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            await ctx.send(f"✅ Guided training of {iterations} iterations completed successfully!")
        else:
            await ctx.send(f"❌ Guided training failed with exit code {process.returncode}.\nError details:\n```\n{stderr.decode(errors='replace')[-1000:]}\n```")
    except Exception as e:
        await ctx.send(f"Failed to launch training: {e}")

@bot.command(name="run_cmd")
async def run_cmd(ctx, *, command: str):
    """Executes a shell command in the workspace and returns the output."""
    await ctx.send(f"💻 Running command: `{command}`...")
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        out = stdout.decode(errors="replace")
        err = stderr.decode(errors="replace")
        msg = f"**Command Exit Code:** `{process.returncode}`\n"
        if out:
            msg += f"**Output:**\n```\n{out[-1500:]}\n```"
        if err:
            msg += f"**Errors:**\n```\n{err[-1500:]}\n```"
        if len(msg) > 2000:
            msg = msg[:1990] + "\n...(truncated)"
        await ctx.send(msg)
    except Exception as e:
        await ctx.send(f"Error executing command: {e}")

import asyncio
import sys


if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_TOKEN is missing in the .env file.")
    else:
        bot.run(TOKEN)
