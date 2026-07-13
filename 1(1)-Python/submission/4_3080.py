from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Iterable


"""
TODO:
- Trie.push 구현하기
- (필요할 경우) Trie에 추가 method 구현하기
"""


T = TypeVar("T")


@dataclass
class TrieNode(Generic[T]):
    body: Optional[T] = None
    children: list[int] = field(default_factory=lambda: [])
    is_end: bool = False


class Trie(list[TrieNode[T]]):
    def __init__(self) -> None:
        super().__init__()
        self.append(TrieNode(body=None))

    def push(self, seq: Iterable[T]) -> None:
        """
        seq: T의 열 (list[int]일 수도 있고 str일 수도 있고 등등...)

        action: trie에 seq을 저장하기
        """
        num = 0
        for letter in seq:
            #children 중 body가 letter인 노드가 있으면 따라가기
            for child in self[num].children:
                if self[child].body == letter:
                    num = child
                    break
            #없으면 새 노드를 만들어서 children에 등록
            else:
                self.append(TrieNode(body=letter))
                self[num].children.append(len(self) - 1)
                num = len(self) - 1
        #seq 전체를 다 따라간 노드가 단어의 끝
        self[num].is_end = True

    def pt(self) -> None:
        print(self)


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