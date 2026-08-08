class ReportCollector:
    """data.json 분석 모드의 케이스별 PASS/FAIL 결과를 모아 요약을 출력한다."""

    def __init__(self):
        self.results = []  # (case_id, passed: bool, reason: str) 튜플 리스트

    def add(self, case_id, passed, reason=""):
        # 케이스 하나의 결과를 기록
        self.results.append((case_id, passed, reason))

    def print_summary(self):
        # 총 테스트 수 / 통과 수 / 실패 수를 계산해 출력
        # 실패 케이스가 있다면 "- case_id: 사유" 형태로 목록 출력
        total = len(self.results)
        passed_count = sum(1 for _, passed, _ in self.results if passed)
        failed_count = total - passed_count

        print(f"총 테스트: {total}개")
        print(f"통과: {passed_count}개")
        print(f"실패: {failed_count}개")

        if failed_count > 0:
            print()
            print("실패 케이스:")
            for case_id, passed, reason in self.results:
                if not passed:
                    print(f"- {case_id}: {reason}")
                    
