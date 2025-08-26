import asyncio
import os

import discord
from discord.ext import commands

import config
from database import db, Profile, User, Channel, Prism

if os.name != "nt":
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

intents = discord.Intents(message_content=True, messages=True, guilds=True, emojis=True)
bot = commands.AutoShardedBot(command_prefix="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                              intents=intents,
                              member_cache_flags=discord.MemberCacheFlags.none(),
                              help_command=None,
                              max_messages=None,
                              chunk_guilds_at_startup=False)

@bot.event
async def setup_hook():
    await bot.load_extension("main")

async def reload():
    try:
        await bot.unload_extension("main")
    except commands.ExtensionNotLoaded:
        pass
    await bot.load_extension("main")

bot.cat_bot_reload_hook = reload  # pyright: ignore

db.connect()
if not db.get_tables():
    db.create_tables([Profile, User, Channel, Prism])
if "prism" not in db.get_tables():
    db.create_tables([Prism])

try:
    bot.run(config.TOKEN)
finally:
    db.close()
