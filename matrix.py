class Matrix:
    """n x n 2차원 데이터(패턴 또는 필터)를 저장하는 데이터 구조."""

    def __init__(self, n, rows):
        # n: 정사각 행렬 크기
        # rows: n x n 형태의 리스트의 리스트
        self.n = n
        self.rows = rows

    def get(self, i, j):
        # (i, j) 위치의 값을 반환
        return self.rows[i][j]

    def set(self, i, j, value):
        # (i, j) 위치에 값을 저장
        self.rows[i][j] = value

    def flatten(self):
        # [보너스] 2차원 리스트를 1차원(길이 N^2) 리스트로 변환
        # i, j -> i * self.n + j 인덱싱 공식 활용
        result = []
        for i in range(self.n):
            for j in range(self.n):
                result.append(self.get(i, j))
        return result

    @classmethod
    def from_console(cls, n, label):
        # label: "필터 A (3줄 입력, 공백 구분)" 같은 안내 문구
        # n줄을 input()으로 입력받아 Matrix 인스턴스로 반환
        #
        # 검증 규칙(최소 기준):
        # - 한 줄에 숫자가 n개가 아니면 재입력 유도
        # - 숫자로 파싱할 수 없는 값이 있으면 재입력 유도
        # - 안내 문구 예: "입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요."
        print(label)
        rows = []

        for _ in range(n):
            while True:
                line = input()
                parts = line.split()

                if len(parts) != n:
                    print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                    continue

                try:
                    row = [float(p) for p in parts]
                except ValueError:
                    print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                    continue
                
                rows.append(row)
                break
        return cls(n, rows)     


    @classmethod
    def from_list(cls, rows):
        # data.json 등에서 읽은 2차원 리스트(rows)로부터 Matrix 생성
        # n은 len(rows)로 결정
        n = len(rows)
        return cls(n, rows)

    def __repr__(self):
        return "\n".join(" ".join(str(value) for value in row) for row in self.rows)
