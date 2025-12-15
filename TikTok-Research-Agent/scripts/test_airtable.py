"""
Airtable 연결 테스트 스크립트

이 스크립트는:
1. .env 파일에서 Airtable 설정 로드
2. Airtable API 연결 테스트
3. tiktok_trends 테이블에 테스트 레코드 생성
4. 데이터 조회 확인
5. 테스트 레코드 삭제

사용법:
    python scripts/test_airtable.py
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from pyairtable import Api

# .env 파일 로드
env_path = project_root.parent / '.env'
load_dotenv(env_path)

# 환경 변수 확인
AIRTABLE_PAT = os.getenv('AIRTABLE_PAT')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

def test_airtable_connection():
    """Airtable 연결 및 기본 CRUD 테스트"""

    print("=" * 60)
    print("🔍 Airtable 연결 테스트 시작")
    print("=" * 60)

    # 환경 변수 확인
    print(f"\n📌 환경 변수 확인:")
    print(f"   AIRTABLE_PAT: {AIRTABLE_PAT[:20]}..." if AIRTABLE_PAT else "   ❌ AIRTABLE_PAT 없음")
    print(f"   AIRTABLE_BASE_ID: {AIRTABLE_BASE_ID}")

    if not AIRTABLE_PAT or not AIRTABLE_BASE_ID:
        print("\n❌ .env 파일에 AIRTABLE_PAT 또는 AIRTABLE_BASE_ID가 없습니다!")
        print("   .env 파일을 확인해주세요.")
        return False

    try:
        # API 초기화
        print("\n🔌 Airtable API 초기화 중...")
        api = Api(AIRTABLE_PAT)

        # tiktok_trends 테이블 연결
        print("📊 tiktok_trends 테이블 연결 중...")
        table = api.table(AIRTABLE_BASE_ID, 'tiktok_trends')

        # 테스트 레코드 데이터
        test_data = {
            "keyword": "#TestHashtag",
            "trend_score": 50,
            "video_count": 100,
            "growth_rate": 10.5,
            "category": "Food",
            "description": "이것은 연결 테스트용 레코드입니다.",
            "collected_at": datetime.now().strftime('%Y-%m-%d'),
            "source": "Test Script",
            "notes": "자동으로 생성되고 삭제됩니다."
        }

        # 1. CREATE: 테스트 레코드 생성
        print("\n✍️  테스트 레코드 생성 중...")
        test_record = table.create(test_data)
        record_id = test_record['id']
        print(f"✅ 테스트 레코드 생성 성공!")
        print(f"   Record ID: {record_id}")
        print(f"   Keyword: {test_record['fields']['keyword']}")
        print(f"   Trend Score: {test_record['fields']['trend_score']}")

        # 2. READ: 데이터 조회
        print("\n📖 데이터 조회 중...")
        records = table.all(max_records=5)
        print(f"✅ 데이터 조회 성공! (총 {len(records)}개 레코드)")

        if len(records) > 0:
            print("\n   최근 레코드:")
            for i, record in enumerate(records[:3], 1):
                fields = record['fields']
                keyword = fields.get('keyword', 'N/A')
                score = fields.get('trend_score', 'N/A')
                print(f"   {i}. {keyword} (Score: {score})")

        # 3. DELETE: 테스트 레코드 삭제
        print(f"\n🗑️  테스트 레코드 삭제 중... (ID: {record_id})")
        table.delete(record_id)
        print("✅ 테스트 레코드 삭제 완료!")

        # 성공 메시지
        print("\n" + "=" * 60)
        print("🎉 Airtable 연결 테스트 통과!")
        print("=" * 60)
        print("\n✅ 다음 단계:")
        print("   1. Python 가상환경 설정")
        print("   2. Docker 설치 및 n8n 실행")
        print("   3. 에이전트 1 개발 시작 (Day 1-2)")
        print("\n")

        return True

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ Airtable 연결 테스트 실패!")
        print("=" * 60)
        print(f"\n에러 내용: {str(e)}")
        print("\n🔍 문제 해결 방법:")
        print("   1. .env 파일에 AIRTABLE_PAT이 올바른지 확인")
        print("   2. AIRTABLE_BASE_ID가 올바른지 확인")
        print("   3. Airtable 테이블 이름이 'tiktok_trends'인지 확인")
        print("   4. Personal Access Token 권한 확인:")
        print("      - data.records:read")
        print("      - data.records:write")
        print("\n")
        return False


def test_research_news_table():
    """research_news 테이블 연결 테스트"""

    print("=" * 60)
    print("🔍 research_news 테이블 테스트 시작")
    print("=" * 60)

    try:
        api = Api(AIRTABLE_PAT)
        table = api.table(AIRTABLE_BASE_ID, 'research_news')

        # 테스트 레코드 생성
        test_data = {
            "title": "테스트 뉴스 제목",
            "url": "https://example.com/test",
            "summary": "이것은 연결 테스트용 뉴스 요약입니다.",
            "sentiment": "Neutral",
            "topic": "Other",
            "published_at": datetime.now().strftime('%Y-%m-%d'),
            "source": "Test Script",
            "notes": "자동 생성/삭제됩니다."
        }

        print("\n✍️  테스트 레코드 생성 중...")
        test_record = table.create(test_data)
        record_id = test_record['id']
        print(f"✅ 레코드 생성 성공! (ID: {record_id})")

        # 삭제
        print("🗑️  테스트 레코드 삭제 중...")
        table.delete(record_id)
        print("✅ 삭제 완료!")

        print("\n🎉 research_news 테이블 테스트 통과!\n")
        return True

    except Exception as e:
        print(f"\n❌ research_news 테이블 테스트 실패: {str(e)}\n")
        return False


if __name__ == "__main__":
    # tiktok_trends 테이블 테스트
    success1 = test_airtable_connection()

    # research_news 테이블 테스트
    if success1:
        success2 = test_research_news_table()
    else:
        success2 = False

    # 종료 코드
    sys.exit(0 if (success1 and success2) else 1)
