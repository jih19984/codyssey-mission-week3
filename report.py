class ReportCollector:
    """data.json 분석 모드의 케이스별 PASS/FAIL 결과를 모아 요약을 출력한다."""

    def __init__(self):
        self.results = []  # (case_id, passed: bool, reason: str) 튜플 리스트

    def add(self, case_id, passed, reason=""):
        # 케이스 하나의 결과를 기록
        pass

    def print_summary(self):
        # 총 테스트 수 / 통과 수 / 실패 수를 계산해 출력
        # 실패 케이스가 있다면 "- case_id: 사유" 형태로 목록 출력
        pass
