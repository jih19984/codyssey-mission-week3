import time


def measure_avg_time_ms(func, args, repeat=10):
    # func(*args)를 repeat회 반복 실행하면서
    # "연산 함수 호출 구간"만 time.perf_counter()로 측정 (입출력 시간은 제외)
    # 총 소요 시간을 repeat로 나눈 평균을 ms 단위로 반환
    start = time.perf_counter()
    for _ in range(repeat):
        func(*args)
    end = time.perf_counter()

    total_ms = (end - start) * 1000
    return total_ms / repeat


def print_performance_table(rows):
    # rows: [(size, avg_ms, op_count), ...] 형태의 리스트
    # "크기(N×N) / 평균 시간(ms) / 연산 횟수(N^2)" 표 형태로 출력
    print(f"{'크기':<10}{'평균 시간 (ms)':<16}{'연산 횟수'}")
    print("-" * 37)
    for size, avg_ms ,op_count in rows:
        label = f"{size}x{size}"
        print(f"{label:<10}{avg_ms:<16.3f}{op_count}")
