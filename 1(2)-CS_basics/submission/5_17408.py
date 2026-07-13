from __future__ import annotations

from typing import TypeVar, Generic, Callable


"""
TODO:
- SegmentTree 구현하기
"""


T = TypeVar("T")
U = TypeVar("U")


class SegmentTree(Generic[T, U]):
    """
    T: 원본 수열의 원소 타입
    U: 트리 노드에 저장되는 타입

    default: U의 항등원 (query 범위 밖의 값과 합쳐도 결과가 안 변하는 값)
    f_conv: 원본 값(T)을 노드 값(U)으로 변환하는 함수
    f_merge: 두 노드 값을 하나로 합치는 함수
    """

    def __init__(
        self,
        arr: list[T],
        default: U,
        f_conv: Callable[[T], U],
        f_merge: Callable[[U, U], U],
    ) -> None:
        self.n = len(arr)
        self.default = default
        self.f_conv = f_conv
        self.f_merge = f_merge

        #리프 개수를 2의 거듭제곱으로 맞추기
        self.size = 1
        while self.size < self.n:
            self.size *= 2

        #tree[1]이 루트, tree[size + i]가 arr[i]에 대응되는 리프
        self.tree: list[U] = [default] * (2 * self.size)
        for i, value in enumerate(arr):
            self.tree[self.size + i] = f_conv(value)
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = f_merge(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, index: int, value: T) -> None:
        """arr[index](0-indexed)를 value로 바꾸고 조상 노드들을 갱신"""
        i = self.size + index
        self.tree[i] = self.f_conv(value)
        i //= 2
        while i >= 1:
            self.tree[i] = self.f_merge(self.tree[2 * i], self.tree[2 * i + 1])
            i //= 2

    def query(self, left: int, right: int) -> U:
        """[left, right) 구간(0-indexed, 반열림)을 f_merge로 합친 값"""
        res_left = self.default
        res_right = self.default
        lo = self.size + left
        hi = self.size + right

        while lo < hi:
            if lo % 2 == 1:  #lo가 오른쪽 자식이면 이 노드만 따로 합치고 다음으로
                res_left = self.f_merge(res_left, self.tree[lo])
                lo += 1
            if hi % 2 == 1:  #hi(미포함)가 오른쪽 자식이면 그 왼쪽 형제를 합침
                hi -= 1
                res_right = self.f_merge(self.tree[hi], res_right)
            lo //= 2
            hi //= 2

        return self.f_merge(res_left, res_right)



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