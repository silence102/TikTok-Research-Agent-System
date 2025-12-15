# Airtable 스키마 정의

## Base 정보
- **Base ID**: `appEIGmZNLYeWLxb5`
- **Base Name**: TikTok Research

---

## 테이블 1: `tiktok_trends`

### 필드 정의

| 필드명 | 타입 | 설명 | 예시 | 필수 |
|--------|------|------|------|------|
| `keyword` | Single line text | 검색한 키워드/해시태그 | "#buldak" | ✅ |
| `trend_score` | Number | 트렌드 점수 (0-100) | 92 | ✅ |
| `video_count` | Number | 해당 키워드 영상 수 | 3500 | ✅ |
| `growth_rate` | Number | 성장률 (%) | 35.2 | ❌ |
| `sample_video_url` | URL | 대표 영상 URL | https://tiktok.com/@user/video/... | ❌ |
| `category` | Single select | 카테고리 | "Food" | ✅ |
| `description` | Long text | 트렌드 설명/인사이트 | "겨울철 스파이시 챌린지..." | ❌ |
| `collected_at` | Date | 수집 일시 | 2025-01-15 | ✅ |
| `source` | Single line text | 데이터 출처 | "Apify" | ✅ |
| `notes` | Long text | 메모/디버깅 정보 | JSON 원본 등 | ❌ |

### Category 옵션
- Food
- Dance
- Comedy
- Review
- Beauty
- Other

### 예시 레코드

```json
{
  "fields": {
    "keyword": "#BuldakChallenge",
    "trend_score": 92,
    "video_count": 3500,
    "growth_rate": 35.2,
    "sample_video_url": "https://www.tiktok.com/@example/video/123",
    "category": "Food",
    "description": "겨울철 스파이시 챌린지가 폭발적으로 성장 중. 마이크로 인플루언서 참여도 높음.",
    "collected_at": "2025-01-15",
    "source": "Apify",
    "notes": "{\"raw_data\": ...}"
  }
}
```

### Python 연동 예시

```python
from pyairtable import Api
import os

api = Api(os.getenv('AIRTABLE_PAT'))
base_id = os.getenv('AIRTABLE_BASE_ID')
table = api.table(base_id, 'tiktok_trends')

# 레코드 생성
table.create({
    "keyword": "#BuldakChallenge",
    "trend_score": 92,
    "video_count": 3500,
    "category": "Food",
    "collected_at": "2025-01-15",
    "source": "Apify"
})

# 최근 7일 데이터 조회
records = table.all(
    formula="IS_AFTER({collected_at}, '2025-01-08')",
    sort=[("trend_score", "desc")],
    max_records=10
)
```

---

## 테이블 2: `research_news`

### 필드 정의

| 필드명 | 타입 | 설명 | 예시 | 필수 |
|--------|------|------|------|------|
| `title` | Single line text | 기사 제목 | "TikTok Shop 수수료 인하" | ✅ |
| `url` | URL | 기사 URL | https://techcrunch.com/... | ✅ |
| `summary` | Long text | 한국어 요약 (200자 이내) | "틱톡 샵이 소규모 크리에이터..." | ✅ |
| `sentiment` | Single select | 감성 분석 | "Positive" | ✅ |
| `topic` | Single select | 주제 분류 | "TikTok" | ✅ |
| `published_at` | Date | 발행일 | 2025-01-12 | ✅ |
| `source` | Single line text | 출처 | "TechCrunch" | ✅ |
| `notes` | Long text | 메모/원문 | 원문 텍스트 등 | ❌ |

### Sentiment 옵션
- Positive
- Neutral
- Negative

### Topic 옵션
- Marketing
- Creator
- TikTok
- Business
- Other

### 예시 레코드

```json
{
  "fields": {
    "title": "TikTok Shop 소규모 크리에이터 수수료 인하",
    "url": "https://techcrunch.com/2025/01/12/tiktok-shop-fees",
    "summary": "틱톡 샵이 1K-50K 팔로워 크리에이터의 수수료를 15%에서 10%로 인하. 마이크로 인플루언서 수익화 기회 확대 예상.",
    "sentiment": "Positive",
    "topic": "TikTok",
    "published_at": "2025-01-12",
    "source": "TechCrunch",
    "notes": "Full article text..."
  }
}
```

### Python 연동 예시

```python
# research_news 테이블
news_table = api.table(base_id, 'research_news')

# 레코드 생성
news_table.create({
    "title": "TikTok Shop 소규모 크리에이터 수수료 인하",
    "url": "https://techcrunch.com/2025/01/12/tiktok-shop-fees",
    "summary": "틱톡 샵이 1K-50K 팔로워 크리에이터의 수수료를 15%에서 10%로 인하...",
    "sentiment": "Positive",
    "topic": "TikTok",
    "published_at": "2025-01-12",
    "source": "TechCrunch"
})

# 최근 뉴스 조회
records = news_table.all(
    formula="IS_AFTER({published_at}, '2025-01-08')",
    sort=[("published_at", "desc")]
)
```

---

## 데이터 아카이빙 전략

Airtable 무료 플랜은 **1,200 rows** 제한이 있습니다.

### 자동 아카이빙 스크립트

```python
import json
from datetime import datetime, timedelta
from pyairtable import Api
import os

def archive_old_data():
    """30일 이상 오래된 데이터를 JSON 백업 후 삭제"""
    api = Api(os.getenv('AIRTABLE_PAT'))
    base_id = os.getenv('AIRTABLE_BASE_ID')

    threshold = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    # tiktok_trends 아카이빙
    trends_table = api.table(base_id, 'tiktok_trends')
    old_records = trends_table.all(
        formula=f"IS_BEFORE({{collected_at}}, '{threshold}')"
    )

    if old_records:
        # JSON 백업
        with open(f'data/archive_trends_{threshold}.json', 'w') as f:
            json.dump(old_records, f, indent=2, ensure_ascii=False)

        # 삭제
        for record in old_records:
            trends_table.delete(record['id'])

        print(f"✅ Archived {len(old_records)} trend records")

    # research_news 아카이빙
    news_table = api.table(base_id, 'research_news')
    old_news = news_table.all(
        formula=f"IS_BEFORE({{published_at}}, '{threshold}')"
    )

    if old_news:
        with open(f'data/archive_news_{threshold}.json', 'w') as f:
            json.dump(old_news, f, indent=2, ensure_ascii=False)

        for record in old_news:
            news_table.delete(record['id'])

        print(f"✅ Archived {len(old_news)} news records")

if __name__ == "__main__":
    archive_old_data()
```

---

## 요약

- **Base ID**: `appEIGmZNLYeWLxb5`
- **테이블 1**: `tiktok_trends` (10개 필드)
- **테이블 2**: `research_news` (8개 필드)
- **무료 플랜 한도**: 1,200 rows
- **아카이빙**: 30일 이상 데이터 자동 백업/삭제
