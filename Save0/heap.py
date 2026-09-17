def iden(x):
    return x

def up(buff, idx, key=iden):
    parent = (idx - 1) // 2
    if parent >= 0 and key(buff[idx]) > key(buff[parent]):
        buff[idx], buff[parent] = buff[parent], buff[idx]
        up(buff, parent, key)

def down(buff, idx, key=iden):
    largest = idx
    left = 2 * idx + 1
    right = 2 * idx + 2
    
    if left < len(buff) and key(buff[left]) > key(buff[largest]):
        largest = left
    if right < len(buff) and key(buff[right]) > key(buff[largest]):
        largest = right
        
    if largest != idx:
        buff[idx], buff[largest] = buff[largest], buff[idx]
        down(buff, largest, key)

def add(buff, val, key=iden):
    buff.append(val)
    up(buff, len(buff) - 1, key)

def poph(buff, key=iden):
    if not buff:
        return None
    if len(buff) == 1:
        return buff.pop()
    
    max_val = buff[0]
    buff[0] = buff.pop()
    down(buff, 0, key)
    return max_val
    
def peek(buff):
    if not buff:
        return None
    return buff[0]
