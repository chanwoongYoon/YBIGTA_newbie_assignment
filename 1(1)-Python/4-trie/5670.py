from lib import Trie
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