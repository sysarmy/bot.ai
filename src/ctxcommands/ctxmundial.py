from src.mundial import mundialfun

async def mundialfunctx(ctx):
    embed = await mundialfun(ctx)
    await ctx.send(embed=embed)
