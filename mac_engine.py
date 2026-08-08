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


def judge(score_a, score_b, label_a, label_b):
    # abs(score_a - score_b) < EPSILON 이면 동점 -> "UNDECIDED" 반환
    # 그렇지 않으면 더 높은 점수의 라벨(label_a 또는 label_b) 반환
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    # 삼항 연산자
    return label_a if score_a > score_b else label_b 
