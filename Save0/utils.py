def move_to(x, y):
    cx, cy = get_pos_x(), get_pos_y()
    dx, dy = cx - x, cy - y
    op={
        'x': {1: West, -1: East},
        'y': {1: South, -1: North}
    }
    for v,d in [(dx, 'x'), (dy, 'y')]:
        while v != 0:
            dir = (v/abs(v))
            move(op[d][dir])
            v += (-1*dir)

def zeroes(length, zero_val = 0):
    ret = []
    for _ in range(length):
        ret.append(zero_val)
    return ret

def is_eq(t, key=None):
    def exec(v):
        if key == None:
            return v == t
        val = v[key]
        return val == t
    return exec

def all_are(itr, fn):
    if len(itr) == 0:
        return False
    for i in itr:
        if not fn(i):
            return False
    return True

def first(itr):
    return itr[0]

def extend(l1, l2):
    for i in l2:
        l1.append(i)
    return l1
