from matrix import Matrix
from mac_engine import compute_score, judge, EPSILON
from data_loader import load_data, extract_size_from_key, iter_pattern_cases, get_filters_for_size
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
        print("=== Mini NPU Simulator ===")
        print()
        print("[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        choice = input("선택: ").strip()

        if choice == "1":
            self.run_user_input_mode()
        elif choice == "2":
            self.run_json_analysis_mode()
        else:
            print("잘못된 선택입니다.")

    def run_user_input_mode(self):
        # [1] 필터 입력: Matrix.from_console(3, "필터 A ...") x2 (A, B)
        # [2] 패턴 입력: Matrix.from_console(3, "패턴 ...")
        # [3] MAC 결과: compute_score(pattern, A), compute_score(pattern, B)
        #     judge()로 A/B/UNDECIDED 판정, 점수/판정 출력
        # [4] 성능 분석(3x3): measure_avg_time_ms로 10회 반복 평균 시간 출력
        print()
        print("#---")
        print("# [1] 필터 입력")
        print("#---")
        filter_a = Matrix.from_console(3, "필터 A (3줄 입력, 공백 구분)")
        filter_b = Matrix.from_console(3, "필터 B (3줄 입력, 공백 구분)")
        print("필터 A, B 저장 완료")

        print()
        print("#---")
        print("# [2] 패턴 입력")
        print("#---")
        pattern = Matrix.from_console(3, "패턴 (3줄 입력, 공백 구분)")

        print()
        print("#---")
        print("# [3] MAC 결과")
        print("#---")
        score_a = compute_score(pattern, filter_a)
        score_b = compute_score(pattern, filter_b)
        result = judge(score_a, score_b, "A", "B")
        avg_ms = measure_avg_time_ms(compute_score, (pattern, filter_a), repeat=10)

        print(f"A 점수: {score_a}")
        print(f"B 점수: {score_b}")
        print(f"연산 시간(평균/10회): {avg_ms:.3f} ms")

        if result == "UNDECIDED":
            print(f"판정: 판정 불가 (|A-B| < {EPSILON})")
        else:
            print(f"판정: {result}")

    def run_json_analysis_mode(self):
        # [1] 필터 로드: load_data() 후 size_5/13/25 필터 로드 완료 메시지 출력
        # [2] 패턴 분석: iter_pattern_cases()로 케이스 순회
        #     - 크기/스키마 문제가 있으면 바로 FAIL 처리 (ReportCollector.add)
        #     - 정상 케이스는 compute_score + judge 수행, expected와 비교해 PASS/FAIL 기록
        # [3] 성능 분석: 3x3(자체 샘플 또는 생성 패턴) + data.json의 5x5/13x13/25x25로 측정,
        #     print_performance_table로 출력
        # [4] 결과 요약: ReportCollector.print_summary() 호출
        print()
        print("#---")
        print("# [1] 필터 로드")
        print("#---")
        data = load_data()
        if data is None:
            print("data.json을 불러올 수 없어 분석을 진행할 수 없습니다.")
            return

        sizes = sorted(data["filters"].keys(), key=extract_size_from_key)
        for size_key in sizes:
            n = extract_size_from_key(size_key)
            print(f"v size_{n} 필터 로드 완료 (Cross, X)")

        print()
        print("#---")
        print("# [2] 패턴 분석 (라벨 정규화 적용)")
        print("#---")
        collector = ReportCollector()

        for case_id, n, input_matrix, expected, error in iter_pattern_cases(data):
            print(f"--- {case_id} ---")

            if error:
                print(f"FAIL - {error}")
                collector.add(case_id, False, error)
                print()
                continue
            
            cross, x = get_filters_for_size(data, n)
            score_cross = compute_score(input_matrix, cross)
            score_x = compute_score(input_matrix, x)
            result = judge(score_cross, score_x, "Cross", "X")
            verdict = "PASS" if result == expected else "FAIL"

            print(f"Cross 점수: {score_cross}")
            print(f"X 점수: {score_x}")
            print(f"판정: {result} | expected: {expected} | {verdict}")
            print()

            if verdict == "PASS":
                collector.add(case_id, True)
            elif result == "UNDECIDED":
                collector.add(case_id, False, "동점(UNDECIDED) 처리 규칙에 따라 FAIL")
            else:
                collector.add(case_id, False, f"판정({result})이 expected({expected})와 다름")

        print("#---")
        print("# [3] 성능 분석 (평균/10회)")
        print("#---")

        sample_3x3 = Matrix.from_list([[0,1,0], [1,1,1], [0,1,0]])
        rows = [(3, measure_avg_time_ms(compute_score, (sample_3x3, sample_3x3), repeat=10), 9)]

        for size_key in sizes:
            n = extract_size_from_key(size_key)
            cross, x = get_filters_for_size(data, n)
            avg_ms = measure_avg_time_ms(compute_score, (cross, cross), repeat=10)
            rows.append((n, avg_ms, n*n))

        print_performance_table(rows)

        print()
        print("#---")
        print("# [4] 결과 요약")
        print("#---")
        collector.print_summary()
