from lib import SegmentTree
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