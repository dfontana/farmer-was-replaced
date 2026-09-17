import heap

WORLD_SIZE = get_world_size()

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

def watered(fn):
    def exec(ctx):
        try_water()
        fn(ctx)
    return exec

def fertilized(fn):
    def exec(ctx):
        fn(ctx)
        use_item(Items.Fertilizer)
    return exec

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
        while True:
            next = heap.poph(sunflowers, first)
            if not next:
                break
            move_to(next[1], next[2])
            while True:
                if can_harvest():
                    harvest()
                    break
        move_to(x, 0)

def alternate(fn1, fn2):
    def exec(ctx):
        if ctx['y'] % 2 == 0:
            fn1(ctx)
        else:
            fn2(ctx)
    return exec

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

def plant_col(fn, x, y):
    bound = WORLD_SIZE - y
    for y_p in range(bound):
        fn({
            'x': x,
            'y': y_p,
            'can_harvest': can_harvest(),
            'ground_type': get_ground_type(),
            'entity_type': get_entity_type()
        })
        if y_p != bound - 1:
            move(North)

def plant_rep(fn_list, x, y):
    for col_fn in fn_list:
        plant_col(col_fn, x, y)
        x += 1
        move_to(x, y)

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

def main():
    move_to(0, 0)
    change_hat(Hats.Traffic_Cone_Stack)
    pet_the_piggy()

    routine = build_pumpkin_patch(6, (0, 0))
    while True:
        # TODO: Layout engine to optimize drone movements. Since all planting assumes
        # south->north,west->east there's a lot of wasted time moving between sub-plots
        # where-as a more efficient zig-zag routine would work better. Even when traversing
        # a pumpkin patch (inbetween direct moves, like the initial planting)
        routine()
        move_to(0, 6)
        plant_rep([
            alternate(tree, bush),
            alternate(bush, tree),
            alternate(tree, bush),
            alternate(fertilized(bush), tree),
            alternate(tree, bush),
            alternate(bush, tree),
        ], 0, 6)
        move_to(6, 0)
        plant_rep([
            watered(carrot),
            watered(carrot),            
            watered(sunflower),
            fertilized(grass),
            fertilized(grass),
            fertilized(grass),
            fertilized(grass),
            fertilized(grass),
            fertilized(grass),
            fertilized(grass),
        ], 6, 0)
        
        
        # TODO: Need layout management
        #     plant_square(3, pumpkin) -> Does not take entire column
        #
        # So logically I want to combinators to finish the columns on that square
        #     plant_plan([
        #       [pumpkin, pumpkin, pumpkin, alternate(tree, grass)], <- Run last function til end of col?
        #       [pumpkin, pumpkin, pumpkin, alternate(grass, tree)],
        #       [pumpkin, pumpkin, pumpkin, carrot)],
        #       [alternate(bush, tree)],
        #       [grass],
        #     ])
        #
        # Pumpkin needs to know when to harvest though, so it wants to know the target size to trigger
        # the harvest condition vs repair condition. You could feed it side length to work from, but then
        # it needs to know the origin or search for the larger pumpkin around it. Alt: you gotta lay out
        # the specific ranges
        #     plant_plan([
        #       (pumpkin,(3,3),(0,0)),
        #       (alternate(tree, grass), None, (0,3)), <-- 'None' signifies what? no size bounds? 
        #       [pumpkin, pumpkin, pumpkin, alternate(grass, tree)],
        #       [pumpkin, pumpkin, pumpkin, carrot)],
        #       [alternate(bush, tree)],
        #       [grass],
        #     ])
        #
        # Current approach is nearly there but since it manipulates movement, we need to orchestrate how the
        # drone moves around the patch between scans better. Eg run the patch routine, then move it from
        # where it's currently at back into the rest of the layout


    

main()
