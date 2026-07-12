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
    children: dict[T, int] = field(default_factory=dict)
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
            #letter가 children안에 있을 때
            if letter in self[num].children:
                num = self[num].children[letter]
            #letter가 children안에 없을 때
            else:
                self.append(TrieNode(body=letter))
                self[num].children[letter] = len(self) - 1
                num = len(self) - 1
        #seq 전체를 다 따라간 노드가 단어의 끝
        self[num].is_end = True

    def pt(self) -> None:
        print(self)