import json

from matrix import Matrix

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
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"data.json을 불러오는데 실패했습니다 : {e}")
        return None


def normalize_label(raw_label):
    # raw_label(예: '+', 'x', 'cross')을 LABEL_MAP을 통해 표준 라벨(Cross/X)로 변환
    # 정의되지 않은 값이 들어오면 어떻게 처리할지도 고려
    return LABEL_MAP.get(str(raw_label).lower())


def extract_size_from_key(key):
    # "size_5_1" -> 5, "size_13_2" -> 13 처럼
    # 패턴 키 문자열에서 크기(N)를 추출해 int로 반환
    parts = key.split("_")
    return int(parts[1])


def get_filters_for_size(data, n):
    # data["filters"]["size_{n}"] 에서 cross/x 필터를 꺼내
    # (cross_matrix, x_matrix) 형태로 반환 (Matrix.from_list 활용)
    size_filters = data["filters"][f"size_{n}"]
    cross = Matrix.from_list(size_filters["cross"])
    x = Matrix.from_list(size_filters["x"])
    return cross, x


def iter_pattern_cases(data):
    # data["patterns"]의 각 항목(case_id, {"input":..., "expected":...})을 순회하며
    # - case_id에서 크기 N 추출
    # - 해당 크기의 filters가 존재하는지 확인
    # - input 배열의 실제 크기가 N과 일치하는지 확인 (불일치 시 별도 표시, 예외로 죽지 않게)
    # 각 케이스에 대해 (case_id, n, input_matrix_or_None, expected_label, error_reason_or_None)
    # 형태로 넘겨주는 제너레이터/리스트를 반환
    cases = []

    for case_id, case in data["patterns"].items():
        n = extract_size_from_key(case_id)
        size_key = f"size_{n}"

        if size_key not in data["filters"]:
            cases.append((case_id, n, None, None, f"{size_key} 필터가 존재하지 않음"))
            continue

        input_rows = case["input"]
        actual_n = len(input_rows)

        if actual_n != n:
            cases.append((case_id, n, None, None, f"크기 불일치: 키는 {n}x{n}인데 input은 {actual_n}x{actual_n}"))
            continue

        input_matrix = Matrix.from_list(input_rows)
        expected_label = normalize_label(case["expected"])

        cases.append((case_id, n, input_matrix, expected_label, None))

    return cases


