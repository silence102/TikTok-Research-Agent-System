# MCP Server Development Skill

## Model Context Protocol (MCP) 개요

MCP는 AI 모델이 외부 데이터 소스와 통신할 수 있게 하는 프로토콜입니다.

### 주요 개념

**Server**: 데이터/기능 제공자
**Client**: AI 모델 (Claude)
**Tools**: Server가 제공하는 기능
**Resources**: Server가 관리하는 데이터

## MCP Server 구조

```python
# server.py
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("my-server")

@app.tool()
async def search_data(query: str) -> list[TextContent]:
    """데이터 검색 도구"""
    results = await database.search(query)
    return [TextContent(text=r) for r in results]

@app.resource("data://trends")
async def get_trends():
    """트렌드 데이터 리소스"""
    return await fetch_latest_trends()

if __name__ == "__main__":
    app.run()
```

## 삼양식품 DXT팀 유즈케이스

### 1. TikTok Trends MCP Server

**목적**: Airtable 데이터를 MCP 프로토콜로 제공

**Tools**:
- `search_trends(keyword: str)`: 키워드로 트렌드 검색
- `get_top_hashtags(limit: int)`: 상위 해시태그 조회

**Resources**:
- `data://trends/daily`: 일일 트렌드
- `data://trends/weekly`: 주간 트렌드

### 2. Creator Economy MCP Server

**Tools**:
- `search_news(topic: str)`: 뉴스 검색
- `summarize_news(news_ids: list[str])`: 뉴스 요약

**Resources**:
- `data://news/latest`: 최신 뉴스

## 개발 워크플로우

### Step 1: Server 구현
```python
# servers/tiktok_mcp/server.py
from mcp.server import Server
from airtable import Airtable

app = Server("tiktok-trends")
db = Airtable(api_key=..., base_id=...)

@app.tool()
async def search_trends(keyword: str, limit: int = 10):
    """틱톡 트렌드 검색"""
    records = db.get_all("tiktok_trends",
                         filter_by_formula=f"SEARCH('{keyword}', hashtag)")
    return records[:limit]
```

### Step 2: 설정 파일
```json
// .claude/mcp-servers.json
{
  "tiktok-trends": {
    "command": "python",
    "args": ["servers/tiktok_mcp/server.py"],
    "env": {
      "AIRTABLE_API_KEY": "${AIRTABLE_API_KEY}"
    }
  }
}
```

### Step 3: 테스트
```bash
# Server 실행
python servers/tiktok_mcp/server.py

# Claude Code에서 테스트
# MCP tool이 자동으로 사용 가능해짐
```

## Best Practices

### 1. 에러 핸들링
```python
@app.tool()
async def search_trends(keyword: str):
    try:
        results = db.search(keyword)
        if not results:
            return [TextContent(text="No results found")]
        return results
    except Exception as e:
        return [TextContent(text=f"Error: {str(e)}")]
```

### 2. 타입 안정성
```python
from pydantic import BaseModel

class TrendQuery(BaseModel):
    keyword: str
    date_from: str | None = None
    date_to: str | None = None
    limit: int = 10

@app.tool()
async def search_trends(query: TrendQuery):
    # 타입 체크 자동 완료
    ...
```

### 3. 캐싱
```python
from functools import lru_cache

@lru_cache(maxsize=100)
async def get_cached_trends():
    # 동일 요청 반복 시 캐시 사용
    return await db.get_all("tiktok_trends")
```
