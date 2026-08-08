from matrix import Matrix
from mac_engine import compute_score, judge, EPSILON
from data_loader import load_data, normalize_label, extract_size_from_key, iter_pattern_cases
from performance import measure_avg_time_ms, print_performance_table
from report import ReportCollector


class NpuSimulatorApp:
    """실행 흐름 전체를 담당하는 오케스트레이터.

    main.py는 이 클래스를 생성하고 run()을 호출하는 역할만 한다.
    """

    def run(self):
        # "=== Mini NPU Simulator ===" 출력
        # [모드 선택] 1) 사용자 입력(3x3)  2) data.json 분석
        # 입력값에 따라 run_user_input_mode() / run_json_analysis_mode() 분기
        pass

    def run_user_input_mode(self):
        # [1] 필터 입력: Matrix.from_console(3, "필터 A ...") x2 (A, B)
        # [2] 패턴 입력: Matrix.from_console(3, "패턴 ...")
        # [3] MAC 결과: compute_score(pattern, A), compute_score(pattern, B)
        #     judge()로 A/B/UNDECIDED 판정, 점수/판정 출력
        # [4] 성능 분석(3x3): measure_avg_time_ms로 10회 반복 평균 시간 출력
        pass

    def run_json_analysis_mode(self):
        # [1] 필터 로드: load_data() 후 size_5/13/25 필터 로드 완료 메시지 출력
        # [2] 패턴 분석: iter_pattern_cases()로 케이스 순회
        #     - 크기/스키마 문제가 있으면 바로 FAIL 처리 (ReportCollector.add)
        #     - 정상 케이스는 compute_score + judge 수행, expected와 비교해 PASS/FAIL 기록
        # [3] 성능 분석: 3x3(자체 샘플 또는 생성 패턴) + data.json의 5x5/13x13/25x25로 측정,
        #     print_performance_table로 출력
        # [4] 결과 요약: ReportCollector.print_summary() 호출
        pass
