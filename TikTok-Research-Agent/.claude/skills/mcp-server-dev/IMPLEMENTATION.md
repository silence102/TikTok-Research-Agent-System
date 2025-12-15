# MCP Server Implementation Guide

## TikTok Research Agent를 위한 MCP Server

### 프로젝트 구조

```
TikTok-Research-Agent/
├── servers/
│   ├── tiktok_mcp/
│   │   ├── server.py
│   │   ├── database.py
│   │   └── requirements.txt
│   └── creator_economy_mcp/
│       ├── server.py
│       └── requirements.txt
└── .claude/
    └── mcp-servers.json
```

### Implementation: TikTok Trends MCP Server

```python
# servers/tiktok_mcp/server.py
import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent, Resource
from database import AirtableClient

app = Server("tiktok-trends")
db = AirtableClient()

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_trends",
            description="Search TikTok trends by keyword",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["keyword"]
            }
        ),
        Tool(
            name="get_top_hashtags",
            description="Get top N hashtags by views",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 10},
                    "date": {"type": "string", "format": "date"}
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_trends":
        keyword = arguments["keyword"]
        limit = arguments.get("limit", 10)

        records = await db.search_trends(keyword, limit)

        if not records:
            return [TextContent(
                type="text",
                text=f"No trends found for keyword: {keyword}"
            )]

        result = "**TikTok Trends**\n\n"
        for r in records:
            result += f"- {r['hashtag']}: {r['views']:,} views\n"
            result += f"  Category: {r['category']}\n"
            result += f"  Collected: {r['collected_at']}\n\n"

        return [TextContent(type="text", text=result)]

    elif name == "get_top_hashtags":
        limit = arguments.get("limit", 10)
        date = arguments.get("date")

        records = await db.get_top_hashtags(limit, date)

        result = "**Top Hashtags**\n\n"
        for i, r in enumerate(records, 1):
            result += f"{i}. {r['hashtag']}: {r['views']:,} views\n"

        return [TextContent(type="text", text=result)]

@app.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="data://trends/latest",
            name="Latest TikTok Trends",
            mimeType="application/json"
        )
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "data://trends/latest":
        trends = await db.get_latest_trends()
        return json.dumps(trends, ensure_ascii=False)

if __name__ == "__main__":
    asyncio.run(app.run())
```

### Database Client

```python
# servers/tiktok_mcp/database.py
import os
from airtable import Airtable

class AirtableClient:
    def __init__(self):
        self.api_key = os.getenv("AIRTABLE_API_KEY")
        self.base_id = os.getenv("AIRTABLE_BASE_ID")
        self.trends_table = Airtable(
            self.base_id,
            "tiktok_trends",
            self.api_key
        )

    async def search_trends(self, keyword: str, limit: int):
        formula = f"SEARCH(LOWER('{keyword}'), LOWER({{hashtag}}))"
        records = self.trends_table.get_all(
            formula=formula,
            max_records=limit,
            sort=[("views", "desc")]
        )
        return [r["fields"] for r in records]

    async def get_top_hashtags(self, limit: int, date: str = None):
        if date:
            formula = f"DATESTR({{collected_at}}) = '{date}'"
            records = self.trends_table.get_all(
                formula=formula,
                max_records=limit,
                sort=[("views", "desc")]
            )
        else:
            records = self.trends_table.get_all(
                max_records=limit,
                sort=[("views", "desc")]
            )
        return [r["fields"] for r in records]

    async def get_latest_trends(self):
        records = self.trends_table.get_all(
            max_records=50,
            sort=[("collected_at", "desc")]
        )
        return [r["fields"] for r in records]
```

### Configuration

```json
// .claude/mcp-servers.json
{
  "mcpServers": {
    "tiktok-trends": {
      "command": "python",
      "args": ["servers/tiktok_mcp/server.py"],
      "env": {
        "AIRTABLE_API_KEY": "${AIRTABLE_API_KEY}",
        "AIRTABLE_BASE_ID": "${AIRTABLE_BASE_ID}"
      }
    },
    "creator-economy": {
      "command": "python",
      "args": ["servers/creator_economy_mcp/server.py"],
      "env": {
        "AIRTABLE_API_KEY": "${AIRTABLE_API_KEY}",
        "AIRTABLE_BASE_ID": "${AIRTABLE_BASE_ID}"
      }
    }
  }
}
```

### Testing

```bash
# 1. Install dependencies
cd servers/tiktok_mcp
pip install -r requirements.txt

# 2. Set environment variables
export AIRTABLE_API_KEY="your_key"
export AIRTABLE_BASE_ID="your_base"

# 3. Run server
python server.py

# 4. In Claude Code, MCP tools are automatically available
# Try: "Search TikTok trends for 'marketing'"
```

## Benefits for Portfolio

1. **Advanced Integration**: MCP는 최신 Claude 기능
2. **Scalability**: 다른 프로젝트에도 재사용 가능
3. **Professional**: 엔터프라이즈급 아키텍처 증명
