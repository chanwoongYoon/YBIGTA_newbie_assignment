from lib import Trie

def count(trie: Trie, query_seq: str) -> int:
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
            if (trie[indx].body == element):
                new_index = indx

        pointer = new_index

    return cnt + int(len(trie[0].children) == 1)

trie = Trie()

trie.push('QWER')
trie.push('QWED')
trie.push('QWRW')
trie.push('OMUS')

print(trie)
print(count(trie,'QWER'))