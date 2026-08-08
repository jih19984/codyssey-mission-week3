import json

DATA_PATH = "data.json"

# expected 값 / filter 키에 등장하는 다양한 표기를 표준 라벨로 매핑
# 표준 라벨은 "Cross", "X" 두 가지만 사용한다
LABEL_MAP = {
    "+": "Cross",
    "cross": "Cross",
    "x": "X",
}


def load_data(path=DATA_PATH):
    # json.load로 data.json을 읽어 dict 반환
    # 파일이 없거나 JSON 파싱에 실패하는 경우를 어떻게 처리할지 고민해볼 것
    # (프로그램이 죽지 않아야 한다는 요구사항과 연결)
    pass


def normalize_label(raw_label):
    # raw_label(예: '+', 'x', 'cross')을 LABEL_MAP을 통해 표준 라벨(Cross/X)로 변환
    # 정의되지 않은 값이 들어오면 어떻게 처리할지도 고려
    pass


def extract_size_from_key(key):
    # "size_5_1" -> 5, "size_13_2" -> 13 처럼
    # 패턴 키 문자열에서 크기(N)를 추출해 int로 반환
    pass


def get_filters_for_size(data, n):
    # data["filters"]["size_{n}"] 에서 cross/x 필터를 꺼내
    # (cross_matrix, x_matrix) 형태로 반환 (Matrix.from_list 활용)
    pass


def iter_pattern_cases(data):
    # data["patterns"]의 각 항목(case_id, {"input":..., "expected":...})을 순회하며
    # - case_id에서 크기 N 추출
    # - 해당 크기의 filters가 존재하는지 확인
    # - input 배열의 실제 크기가 N과 일치하는지 확인 (불일치 시 별도 표시, 예외로 죽지 않게)
    # 각 케이스에 대해 (case_id, n, input_matrix_or_None, expected_label, error_reason_or_None)
    # 형태로 넘겨주는 제너레이터/리스트를 반환
    pass
