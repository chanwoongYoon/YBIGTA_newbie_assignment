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


"""
TODO:
- 일단 Trie부터 구현하기
- count 구현하기
- main 구현하기
"""


def count(trie: Trie[str], query_seq: str) -> int:
    """
    trie - 이름 그대로 trie
    query_seq - 단어 ("hello", "goodbye", "structures" 등)

    returns: query_seq의 단어를 입력하기 위해 버튼을 눌러야 하는 횟수
    """
    pointer = 0
    cnt = 0

    for element in query_seq:
        if len(trie[pointer].children) > 1 or trie[pointer].is_end:
            cnt += 1
        for indx in trie[pointer].children:
            if trie[indx].body == element:
                pointer = indx
                break

    return cnt + int(len(trie[0].children) == 1)


def main() -> None:
    data = sys.stdin.read().split()
    idx = 0
    answers: list[str] = []

    while idx < len(data):
        n = int(data[idx])
        idx += 1
        words = data[idx:idx + n]
        idx += n

        trie: Trie[str] = Trie()
        for word in words:
            trie.push(word)

        total = sum(count(trie, word) for word in words)
        answers.append(f"{total / n:.2f}")

    print("\n".join(answers))


if __name__ == "__main__":
    main()