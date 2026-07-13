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
    길이 m+n 배열에서 DVD가 있는 칸을 1로 두는 합 세그먼트 트리를 유지한다.
    앞쪽 m칸은 꺼낸 DVD를 새로 올릴 빈 자리, 뒤쪽 n칸이 초기 상태(1번이 맨 위).
    영화를 볼 때마다: 내 위치 앞 구간의 합(= 위에 있는 DVD 수)을 출력하고,
    현재 칸을 0으로, 맨 위의 새 칸을 1로 갱신한다.
    """
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx])
    idx += 1
    results: list[str] = []

    for _ in range(t):
        n, m = int(data[idx]), int(data[idx + 1])
        idx += 2
        movies = [int(x) for x in data[idx:idx + m]]
        idx += m

        tree: SegmentTree[int, int] = SegmentTree(
            [0] * m + [1] * n, 0, lambda x: x, lambda a, b: a + b
        )
        pos = [0] * (n + 1)
        for movie_num in range(1, n + 1):
            pos[movie_num] = m + movie_num - 1

        top = m
        answers: list[str] = []
        for movie in movies:
            p = pos[movie]
            answers.append(str(tree.query(0, p)))
            tree.update(p, 0)
            top -= 1
            pos[movie] = top
            tree.update(top, 1)

        results.append(" ".join(answers))

    print("\n".join(results))


if __name__ == "__main__":
    main()