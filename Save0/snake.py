from utils import *

def get_hamiltonian_move(head, body, size):
    # head is the (x, y) location of the head
    # body sequence of coordiantes forming body, with head at the last index
    # Return (status, Dir) -> 0 = done, 1 = continue
    w, h = (size, size)
    x, y = head
    
    # If the body fills the entire grid, you have achieved max length!
    if len(body)+1 >= w * h:
        return (0, None)

    # Step 1: Map every hard coordinate to a sequential step in the closed loop
    def get_step_index(cx, cy):
        if cy == 0:
            # The bottom row (y=0) is our safe highway back to the origin
            # Moving West: from (w-1, 0) all the way down to (0,0)
            return (w - 1) - cx
        else:
            # Rows 1 through h-1 form a winding snake pattern moving North and South
            # Columns are processed from left to right (x = 0 to w-1)
            base_steps = w  # The steps reserved for the bottom row highway
            if cx % 2 == 0:
                # Even columns (0, 2, 4...) wind North: from y=1 up to y=h-1
                return base_steps + cx * (h - 1) + (cy - 1)
            else:
                # Odd columns (1, 3, 5...) wind South: from y=h-1 down to y=1
                return base_steps + cx * (h - 1) + (h - 1 - cy)

    # Step 2: Find the step index of the current head position
    current_step = get_step_index(x, y)
    next_step = (current_step + 1) % (w * h)

    # Step 3: Determine which coordinate matches the next sequential step
    # Check all 4 adjacent moves (including grid wrap-around)
    moves = {
        East:  (x + 1, y),
        West:  (x - 1, y),
        North: (x, y + 1),
        South: (x, y - 1),
    }

    for direction in moves:
        (cx, cy) = moves[direction]
        if 0 <= cx < w and 0 <= cy < h:
            if get_step_index(cx, cy) == next_step:
                return (1, direction)

    return (0, None)


def build_snake(sz):
    set_world_size(sz)
    def solve():
        head = (0, 0)
        body = [head]
        while True:
            is_done, dir = get_hamiltonian_move(head, body, sz)
            if is_done == 0:
                return
            if move(dir):
                head = (get_pos_x(), get_pos_y())
                if measure() != None:
                    body.append(head)

    def exec():
        move_to(0, 0)
        while True:
            if num_items(Items.Cactus) < 16:
                continue
            change_hat(Hats.Dinosaur_Hat)
            solve()
            change_hat(Hats.Traffic_Cone_Stack)
            move_to(0, 0)

    return exec

