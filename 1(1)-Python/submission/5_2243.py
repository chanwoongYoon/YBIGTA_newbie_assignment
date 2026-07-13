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


def main() -> None:
    """
    맛 번호(1~1,000,000)별 사탕 개수를 리프로 갖는 합 세그먼트 트리를 유지한다.
    - 1 B: 루트에서 왼쪽 자식의 합과 B(순위)를 비교하며 내려가 B번째 사탕의 리프를 찾고, 개수를 1 줄인다.
    - 2 B C: 맛 B의 개수에 C를 더한다.
    """
    input = sys.stdin.readline
    MAX_TASTE = 1_000_000

    counts = [0] * (MAX_TASTE + 1)
    tree: SegmentTree[int, int] = SegmentTree(
        [0] * MAX_TASTE, 0, lambda x: x, lambda a, b: a + b
    )

    n = int(input())
    answers: list[str] = []

    for _ in range(n):
        query = [*map(int, input().split())]

        if query[0] == 1:
            rank = query[1]
            i = 1
            while i < tree.size:
                if tree.tree[2 * i] >= rank:
                    i = 2 * i
                else:
                    rank -= tree.tree[2 * i]
                    i = 2 * i + 1
            taste = i - tree.size + 1
            answers.append(str(taste))
            counts[taste] -= 1
            tree.update(taste - 1, counts[taste])
        else:
            taste, delta = query[1], query[2]
            counts[taste] += delta
            tree.update(taste - 1, counts[taste])

    print("\n".join(answers))


if __name__ == "__main__":
    main()