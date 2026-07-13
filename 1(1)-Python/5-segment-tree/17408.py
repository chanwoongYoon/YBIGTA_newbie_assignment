from lib import SegmentTree
import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


class Pair(tuple[int, int]):
    """
    힌트: 2243, 3653에서 int에 대한 세그먼트 트리를 만들었다면 여기서는 Pair에 대한 세그먼트 트리를 만들 수 있을지도...?
    """
    def __new__(cls, a: int, b: int) -> 'Pair':
        return super().__new__(cls, (a, b))

    @staticmethod
    def default() -> 'Pair':
        """
        기본값
        이게 왜 필요할까...?
        """
        return Pair(0, 0)

    @staticmethod
    def f_conv(w: int) -> 'Pair':
        """
        원본 수열의 값을 대응되는 Pair 값으로 변환하는 연산
        이게 왜 필요할까...?
        """
        return Pair(w, 0)

    @staticmethod
    def f_merge(a: 'Pair', b: 'Pair') -> 'Pair':
        """
        두 Pair를 하나의 Pair로 합치는 연산
        이게 왜 필요할까...?
        """
        return Pair(*sorted([*a, *b], reverse=True)[:2])

    def sum(self) -> int:
        return self[0] + self[1]


def main() -> None:
    """
    각 노드가 (구간 최댓값, 구간 2번째 최댓값) Pair를 갖는 세그먼트 트리를 유지한다.
    - 1 i v: A[i]를 v로 갱신
    - 2 l r: [l, r] 구간 Pair의 두 값의 합(= 최대 Ai + Aj)을 출력
    """
    data = sys.stdin.read().split()
    idx = 0

    n = int(data[idx])
    idx += 1
    arr = [int(x) for x in data[idx:idx + n]]
    idx += n
    m = int(data[idx])
    idx += 1

    tree: SegmentTree[int, Pair] = SegmentTree(
        arr, Pair.default(), Pair.f_conv, Pair.f_merge
    )

    answers: list[str] = []
    for _ in range(m):
        q, a, b = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
        idx += 3
        if q == 1:
            tree.update(a - 1, b)
        else:
            answers.append(str(tree.query(a - 1, b).sum()))

    print("\n".join(answers))


if __name__ == "__main__":
    main()