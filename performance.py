import time


def measure_avg_time_ms(func, args, repeat=10):
    # func(*args)를 repeat회 반복 실행하면서
    # "연산 함수 호출 구간"만 time.perf_counter()로 측정 (입출력 시간은 제외)
    # 총 소요 시간을 repeat로 나눈 평균을 ms 단위로 반환
    pass


def print_performance_table(rows):
    # rows: [(size, avg_ms, op_count), ...] 형태의 리스트
    # "크기(N×N) / 평균 시간(ms) / 연산 횟수(N^2)" 표 형태로 출력
    pass
