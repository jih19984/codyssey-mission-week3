# 트러블슈팅

개발 중 겪은 이슈와 해결 과정을 기록한다.

## 1. `Matrix.flatten()`이 `None`을 반환함

### 문제
`m.flatten()`을 호출했더니 `[1, 2, 3, ...]`이 아니라 `None`이 나왔다.

### 원인
이중 for문으로 `result` 리스트를 다 채워놓고 정작 `return result`를 빼먹었다. 파이썬은 함수 끝까지
`return`을 못 만나면 자동으로 `None`을 반환한다.

### 해결
함수 맨 끝에 `return result` 추가.

## 2. `Matrix.from_console()`이 잘못된 길이의 행을 그냥 받아버림

### 문제
3×3 입력에서 숫자를 2개만 입력해도 에러 메시지만 찍고 재입력 없이 그냥 다음 줄로 넘어갔다. 결과적으로
길이가 3이 아닌 행이 저장됨.

### 원인
`if len(parts) != n:` 블록에서 에러 메시지는 출력했지만 `continue`가 빠져 있어서, 검증에 실패해도 코드가
그대로 아래 `try` 블록까지 흘러 내려가 잘못된 길이의 값을 그대로 `rows`에 추가해버렸다.

### 해결
개수 불일치 분기에도 숫자 파싱 실패 분기와 동일하게 `continue`를 추가해서, 같은 줄을 다시 입력받도록 함.

## 3. `mac_engine.compute_score()`에서 `AttributeError: 'Matrix' object has no attribute 'j'`

### 문제
`compute_score(pattern, filter_)` 호출 시 `'Matrix' object has no attribute 'j'` 에러로 죽음.

### 원인
안쪽 for문을 `for j in range(pattern.j):`로 써서, 반복 변수 이름(`j`)과 `Matrix`의 속성을 착각했다.
`Matrix`엔 `.n`(크기)만 있고 `.j`라는 속성은 없다.

### 해결
`for j in range(pattern.n):`으로 수정 (바깥 for문의 `pattern.n`과 동일하게).

## 4. `data_loader.load_data()` 실패 메시지에 `{e}`가 그대로 찍힘

### 문제
존재하지 않는 파일 경로로 `load_data()`를 호출했을 때, 에러 메시지가 `data.json을 불러오는데
실패했습니다 : {e}`처럼 변수가 치환되지 않고 그대로 출력됐다.

### 원인
`print("...{e}")`에서 문자열 앞에 `f`를 붙이지 않아 f-string이 아닌 일반 문자열이 됐다. 일반 문자열
안의 `{e}`는 그냥 텍스트로 취급된다.

### 해결
`print(f"...{e}")`로 `f` 접두사 추가.

## 5. `ReportCollector.print_summary()`에서 `ValueError: too many values to unpack`

### 문제
`print_summary()` 호출 시 `too many values to unpack (expected 2)` 에러 발생.

### 원인
`self.results`엔 `(case_id, passed, reason)` 3개짜리 튜플이 들어가는데, 통과 개수를 셀 때
`for _, passed in self.results`처럼 2개로만 언패킹하려고 했다.

### 해결
`for _, passed, _ in self.results`로 변수 3개로 맞춰서 언패킹.

## 6. `app.py`에서 `get_filters_for_size`를 썼는데 import가 안 돼 있었음

### 문제
`app.py`에서 `get_filters_for_size(data, n)`를 호출하는 코드를 썼는데, 실행하면 이름을 못 찾는 문제가
있었다.

### 원인
`data_loader.py`엔 함수가 정의돼 있었지만, `app.py` 상단의 `from data_loader import ...` 목록에
`get_filters_for_size`를 빠뜨렸다.

### 해결
import 목록에 `get_filters_for_size` 추가. 겸사겸사 `app.py`에서 안 쓰던 `normalize_label` import는 제거.

## 7. FAIL 사유 메시지에서 괄호 짝이 안 맞음

### 문제
`app.py`의 FAIL 사유 문자열이 `f"판정({result}이 expected({expected})와 다름"`으로, `{result}` 뒤에
닫는 괄호 `)`가 빠져 있었다. 실행은 되지만(파이썬 문법 에러는 아님) 메시지가
`판정(Cross이 expected(X)와 다름`처럼 어색하게 출력될 상황이었다. 현재 `data.json` 테스트 케이스로는
이 분기(판정은 났는데 expected와 다른 경우)가 한 번도 안 걸려서 뒤늦게 코드 리뷰로 발견했다.

### 원인
단순 오타. f-string 안의 텍스트는 파이썬이 괄호 짝을 검사해주지 않기 때문에 실행 자체는 멀쩡히 됐다.

### 해결
`f"판정({result})이 expected({expected})와 다름"`으로 괄호 추가.

## 8. 성능 표 헤더에 "ms" 대신 "ㅡs"가 찍힘

### 문제
`print_performance_table()`의 헤더가 `평균 시간 (ㅡs)`로 출력됐다.

### 원인
한글 입력 상태에서 `(ms)`를 치다가 `m`이 한글 자모 `ㅡ`로 입력된 오타.

### 해결
`(ms)`로 수정.

## 9. [보너스] "1차원 배열 최적화"가 처음엔 오히려 더 느리게 측정됨

### 문제
`Matrix.flatten()` 기반의 `compute_score_flat()`을 만들어서 기존 2차원 버전과 성능을 비교했더니,
1차원 방식이 모든 크기에서 오히려 더 느리게 나왔다(예: 25×25에서 2D 0.0896ms vs 1D 0.1191ms).

### 원인
`measure_avg_time_ms(compute_score_flat, (a, b), repeat=10)`처럼 측정하면, `compute_score_flat()`
호출 한 번마다 `flatten()`이 매번 새로 O(N²) 변환을 수행한다. 즉 "변환 비용 + MAC 연산 비용"을 매번 지불하는
셈이라, 변환 없이 바로 계산하는 2차원 방식보다 손해를 보는 게 당연했다.

### 해결
`flatten()` 변환을 반복 측정 루프 바깥에서 미리 한 번만 해두고, "순수 MAC 루프"만 따로 떼어내 다시
측정했다. 그 결과 1차원 루프가 2차원 루프보다 약 3.5~4.7배 빨랐다 — `get(i, j)` 메서드 호출과 이중
인덱싱(`self.rows[i][j]`) 오버헤드가 없어졌기 때문으로 보인다. 이 경험으로 "최적화 기법 자체는 옳아도,
어디서 비용을 지불하느냐(매 호출마다 vs 한 번만)에 따라 결과가 정반대로 나올 수 있다"는 걸 확인했다.
자세한 수치는 README.md의 "보너스 구현" 섹션 참고.
