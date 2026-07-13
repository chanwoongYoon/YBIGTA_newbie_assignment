from lib import SegmentTree
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