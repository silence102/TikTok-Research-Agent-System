# MCP Protocol Reference

## MCP 메시지 흐름

```
Client (Claude)          Server (MCP)
    |                         |
    |--- list_tools() ------> |
    | <-- Tool[] ------------ |
    |                         |
    |--- call_tool() -------> |
    | <-- TextContent[] ----- |
    |                         |
    |--- list_resources() --> |
    | <-- Resource[] -------- |
    |                         |
    |--- read_resource() ---> |
    | <-- string ------------ |
```

## Tool Schema

### Tool Definition

```python
Tool(
    name="tool_name",
    description="What this tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Parameter description"
            },
            "param2": {
                "type": "integer",
                "default": 10
            }
        },
        "required": ["param1"]
    }
)
```

### Tool Response

```python
[
    TextContent(
        type="text",
        text="Response content here"
    )
]
```

## Resource Schema

### Resource Definition

```python
Resource(
    uri="data://category/resource-name",
    name="Human-readable name",
    mimeType="application/json",
    description="Optional description"
)
```

### URI Patterns

- `data://trends/latest`: 최신 트렌드
- `data://trends/daily/{date}`: 특정 날짜
- `data://news/{category}`: 카테고리별 뉴스

## Error Handling

### Server-side Errors

```python
from mcp.types import McpError

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        # Tool logic
        ...
    except ValueError as e:
        raise McpError(
            code=-32602,  # Invalid params
            message=str(e)
        )
    except Exception as e:
        raise McpError(
            code=-32603,  # Internal error
            message="Internal server error"
        )
```

### Client-side Handling

Claude automatically handles MCP errors and informs the user.

## Best Practices

### 1. Tool Naming
- Use snake_case
- Be descriptive: `search_trends` not `search`
- Group related tools: `trends_search`, `trends_top`

### 2. Description Writing
```python
# Good
description="Search TikTok trends by keyword, returning up to N results sorted by views"

# Bad
description="Search"
```

### 3. Parameter Validation
```python
@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search_trends":
        keyword = arguments.get("keyword", "").strip()
        if not keyword:
            return [TextContent(
                type="text",
                text="Error: keyword parameter is required"
            )]

        limit = arguments.get("limit", 10)
        if limit < 1 or limit > 100:
            return [TextContent(
                type="text",
                text="Error: limit must be between 1 and 100"
            )]
```

### 4. Response Formatting
```python
# Markdown formatting for better readability
result = """
**Search Results for '{keyword}'**

Found {count} trends:

1. **{hashtag1}**
   - Views: {views1:,}
   - Category: {category1}

2. **{hashtag2}**
   - Views: {views2:,}
   - Category: {category2}

Source: Airtable (Updated: {timestamp})
"""
```

## Security Considerations

### 1. API Key Protection
```python
# Never expose API keys in responses
# Use environment variables
api_key = os.getenv("AIRTABLE_API_KEY")
```

### 2. Input Sanitization
```python
import re

def sanitize_keyword(keyword: str) -> str:
    # Remove special characters
    return re.sub(r'[^\w\s-]', '', keyword)
```

### 3. Rate Limiting
```python
from asyncio import Semaphore

rate_limiter = Semaphore(5)  # Max 5 concurrent requests

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    async with rate_limiter:
        # Tool logic
        ...
```
