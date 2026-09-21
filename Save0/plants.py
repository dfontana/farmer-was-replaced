from utils import move_to, first, zeroes, all_are, is_eq
import heap

def get_ctx(x, y):
    return {
        'x': x,
        'y': y,
        'can_harvest': can_harvest(),
        'ground_type': get_ground_type(),
        'entity_type': get_entity_type()
    }

def try_water():
    if get_water() < 0.5:
        use_item(Items.Water)

def try_harvest():
    if can_harvest():
        harvest()

def grass(ctx):
    if ctx['can_harvest']:
        harvest()
    if ctx['ground_type'] != Grounds.Grassland:
        till()
    plant(Entities.Grass)

def bush(ctx):
    # cost == Free
    if ctx['can_harvest']:
        harvest()
    if ctx['ground_type'] != Grounds.Grassland:
        till()
    plant(Entities.Bush)

def tree(ctx):
    # cost == Free
    if ctx['can_harvest']:
        harvest()
    if ctx['ground_type'] != Grounds.Grassland:
        till()
    plant(Entities.Tree)

def carrot(ctx):
    # Cost == 8 grass, 8 wood
    if ctx['can_harvest']:
        harvest()
    if ctx['ground_type'] != Grounds.Soil:
        till()
    plant(Entities.Carrot)

# heap of {pedals,x,y}
sunflowers = []
tracked_sunflowers = {}
def sunflower(ctx):
    x = ctx['x']
    y = ctx['y']
    ground_type = ctx['ground_type']
    entity_type = ctx['entity_type']
    iden = (x, y)
    if ground_type != Grounds.Soil:
        till()
    if entity_type != Entities.Sunflower:
        plant(Entities.Sunflower)
        tracked_sunflowers[iden] = True
        heap.add(sunflowers, (measure(), x, y), first)
    elif iden not in tracked_sunflowers:
        tracked_sunflowers[iden] = True
        heap.add(sunflowers, (measure(), x, y), first)
    if len(sunflowers) == len(tracked_sunflowers):
        sx, sy = get_pos_x(), get_pos_y()
        while True:
            next = heap.poph(sunflowers, first)
            if not next:
                break
            move_to(next[1], next[2])
            while True:
                if can_harvest():
                    harvest()
                    break
        move_to(sx, sy)

def build_pumpkin_patch(size, root):
    ps = {'s': zeroes(size*size)}

    def routine():
        # Need to know when entire patch is grown before harvest
        # Patch state tracks this for us --> flat row-major array
        #   xd,yd -> ps[yd*size+xd]
        #   0 == unknown
        #   1 == planted
        #   2 == can harvest
        x, y = root[0], root[1]
        for xd in range(size):
            for yd in range(size):
                state = ps['s'][yd*size + xd]
                if state == 2:
                    continue

                # Need to investigate the state
                move_to(x+xd, y+yd)
            
                if state == 0:
                    # Detect & repair state
                    if get_ground_type() != Grounds.Soil:
                        till()
                    if get_entity_type() == Entities.Pumpkin:
                        ps['s'][yd*size + xd] = 1
                        if can_harvest():
                            ps['s'][yd*size + xd] = 2
                        else:
                            try_water()
                    elif plant(Entities.Pumpkin):
                            ps['s'][yd*size + xd] = 1
                            try_water()
                if state == 1:
                    # Did it grow or die?
                    if get_entity_type() == Entities.Dead_Pumpkin:
                        # Repair
                        if plant(Entities.Pumpkin):
                            try_water()
                            ps['s'][yd*size + xd] = 1
                    elif can_harvest():
                        # It's ready
                        ps['s'][yd*size + xd] = 2
            
        if all_are(ps['s'], is_eq(2)):
            try_harvest()
            ps['s'] = zeroes(size*size)

    return routine

def build_cacti_patch(size, root):
    x, y = root[0], root[1]

    def needs_swap(delta, dir):
        return delta < size and measure() > (measure(dir) or 0)
    
    def sort_p():
        def sort_s(x, y, dir):
            def exec():
                while True:
                    is_sorted = True
                    move_to(x, y)
                    for delta in range(size-1):
                        # Am I sorted?
                        if needs_swap(delta, dir):
                            is_sorted = False
                            swap(dir)
                        move(dir)
                    if is_sorted:
                        break
            return exec

        for xm, ym, dir in [(0, 1, East), (1, 0, North)]:
            drones = []
            v = size-1
            move_to(x, y)
            while True:
                if v < 0:
                    break
                drone = spawn_drone(sort_s(x+(xm*v), y+(ym*v), dir))
                if drone:
                    v -= 1
                    drones.append(drone)
            for d in drones:
                wait_for(d)

    def routine():
        def grow_col(x, y):
            def exec():
                while True:
                    is_grown = True
                    move_to(x, y)
                    for _ in range(size):
                        if get_ground_type() != Grounds.Soil:
                            till()
                        if get_entity_type() == Entities.Cactus:
                            if not can_harvest():
                                try_water()
                                is_grown = False
                        elif plant(Entities.Cactus):
                            try_water()
                            is_grown = False
                        move(North)
                    if is_grown:
                        break
            return exec

        drones = []
        v = size-1
        move_to(x, y)
        while True:
            if v < 0:
                break
            drone = spawn_drone(grow_col(x+v, y))
            if drone:
                v -= 1
                drones.append(drone)
        for d in drones:
            wait_for(d)
            
        sort_p()
        try_harvest()

    return routine

def watered(fn):
    def exec(ctx):
        try_water()
        fn(ctx)
    return exec

def fertilized(fn):
    def exec(ctx):
        fn(ctx)
        if num_items(Items.Fertilizer) > 0:
            use_item(Items.Fertilizer)
    return exec

def alternate(fn1, fn2):
    def exec(ctx):
        if ctx['y'] % 2 == 0:
            fn1(ctx)
        else:
            fn2(ctx)
    return exec
