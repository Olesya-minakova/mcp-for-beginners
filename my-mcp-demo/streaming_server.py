@mcp.tool()
async def process_documents(ctx):
    for i in range(1, 6):
        await ctx.info(f"Processing document {i}/5")

    return "Done"