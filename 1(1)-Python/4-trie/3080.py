from lib import Trie
import sys
import math


"""
TODO:
- 일단 lib.py의 Trie Class부터 구현하기
- main 구현하기

힌트: 한 글자짜리 자료에도 그냥 str을 쓰기에는 메모리가 아깝다...
"""


def main() -> None:
    input = sys.stdin.readline
    MOD = 1_000_000_007

    n = int(input())
    trie: Trie[int] = Trie()
    for _ in range(n):
        name = input().rstrip()
        trie.push(map(ord, name))  # str 대신 int로 변환해 저장 (메모리 절약)

    tot = 1
    for node in trie:
        # 이 노드에서 뻗어나가는 가짓수: 자식들 + (여기서 끝나는 이름이 있으면 +1)
        k = len(node.children) + (1 if node.is_end else 0)
        tot = tot * math.factorial(k) % MOD

    print(tot)


if __name__ == "__main__":
    main()