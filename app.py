import discord
from discord.ext import commands

# ===== INTENTS =====
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== CONFIG =====
config = {
    "og_role": None,
    "viewer_role": None,
    "limit": 100
}

# ===== READY =====
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# ===== AUTO ROLE ON JOIN =====
@bot.event
async def on_member_join(member):
    if not config["og_role"] or not config["viewer_role"]:
        return

    guild = member.guild
    og_role = guild.get_role(config["og_role"])
    viewer_role = guild.get_role(config["viewer_role"])
    limit = config["limit"]

    # Count current OG members
    count = sum(1 for m in guild.members if og_role in m.roles)

    if count < limit:
        await member.add_roles(og_role)

        position = count + 1
        msg = f"🎉 You are the **#{position} OG member**!"

    else:
        await member.add_roles(viewer_role)
        msg = "😢 OG spots are full — you are a Viewer."

    try:
        await member.send(msg)
    except:
        print(f"Could not DM {member}")
        
# ===== ADMIN CHECK =====
def is_admin():
    async def predicate(ctx):
        return ctx.guild is not None and ctx.author.guild_permissions.administrator
    return commands.check(predicate)

# ===== ADMIN COMMANDS =====
@bot.command()
@is_admin()
async def setroles(ctx, og: discord.Role, viewer: discord.Role):
    config["og_role"] = og.id
    config["viewer_role"] = viewer.id
    await ctx.send("✅ OG and Viewer roles set!")

@bot.command()
@is_admin()
async def setlimit(ctx, number: int):
    config["limit"] = number
    await ctx.send(f"✅ Limit set to {number}")

# ===== ERROR HANDLER =====
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ Admins only.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Missing arguments.")
    else:
        raise error

# ===== RUN =====
bot.run("YOUR_BOT_TOKEN_HERE")
