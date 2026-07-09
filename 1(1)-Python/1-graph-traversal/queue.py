from collections import deque

queue = deque([1])
print(queue)

queue.append(3)
queue.append(4)
queue.append(6)

print(queue)

now_node = queue.popleft()
print(now_node)
print(queue)