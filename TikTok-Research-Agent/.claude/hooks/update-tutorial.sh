#!/bin/bash
# Tutorial.md Auto-Update Hook
# This hook runs after each conversation session to update Tutorial.md

TUTORIAL_PATH="../TikTok-Research-Agent/docs/Tutorial.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Check if Tutorial.md exists
if [ ! -f "$TUTORIAL_PATH" ]; then
    echo "⚠️  Tutorial.md not found at $TUTORIAL_PATH"
    exit 1
fi

# Add session completion log to Tutorial.md
echo "" >> "$TUTORIAL_PATH"
echo "---" >> "$TUTORIAL_PATH"
echo "" >> "$TUTORIAL_PATH"
echo "## 📝 Session Log" >> "$TUTORIAL_PATH"
echo "" >> "$TUTORIAL_PATH"
echo "**Last Updated**: $TIMESTAMP" >> "$TUTORIAL_PATH"
echo "" >> "$TUTORIAL_PATH"
echo "이 문서는 Claude Code 세션 종료 시 자동으로 업데이트됩니다." >> "$TUTORIAL_PATH"

echo "✅ Tutorial.md updated successfully at $TIMESTAMP"
