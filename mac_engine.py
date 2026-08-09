# 두 점수가 사실상 같다고 볼 허용오차(부동소수점 비교 정책)
EPSILON = 1e-9


def compute_score(pattern, filter_):
    # pattern, filter_: Matrix 인스턴스 (크기가 같다고 가정)
    # 위치별로 곱한 뒤 모두 더하는 MAC(Multiply-Accumulate) 연산을
    # 반복문으로 직접 구현한다 (NumPy 등 외부 라이브러리 금지)
    # 반환: 점수 (float 가능)
    score = 0
    for i in range(pattern.n):
        for j in range(pattern.n):
            score += pattern.get(i, j) * filter_.get(i, j)
    return score


def compute_score_flat(pattern_flat, filter_flat):
    # [보너스] 2차원 get(i, j) 대신 1차원(flatten된) 배열을 받아
    # 단일 for문으로 MAC 연산을 수행 (메모리 접근 패턴 단순화)
    #
    # 주의: 인자로 Matrix가 아니라 이미 flatten()된 리스트를 받는다.
    # flatten() 변환 자체를 이 함수 안에서 매번 하면(호출마다 O(N^2) 변환 비용이 추가로 붙어)
    # 오히려 compute_score()보다 느려진다 — 변환은 호출자가 한 번만 해서 넘겨줘야 이득이다.
    score = 0
    for idx in range(len(pattern_flat)):
        score += pattern_flat[idx] * filter_flat[idx]
    return score


def judge(score_a, score_b, label_a, label_b):
    # abs(score_a - score_b) < EPSILON 이면 동점 -> "UNDECIDED" 반환
    # 그렇지 않으면 더 높은 점수의 라벨(label_a 또는 label_b) 반환
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    # 삼항 연산자
    return label_a if score_a > score_b else label_b 
