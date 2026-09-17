from utils import move_to, extend
from maze import step_maze
from plants import *

WORLD_SIZE = get_world_size()

def plant_col(fn, x, y):
    bound = WORLD_SIZE - y
    for y_p in range(bound):
        fn(get_ctx(x, y+y_p))
        if y_p != bound - 1:
            move(North)

def plant_rep(fn_list, x, y):
    for col_fn in fn_list:
        plant_col(col_fn, x, y)
        x += 1
        if x != WORLD_SIZE:
            move_to(x, y)

def mazes():
    def sleep(n):
        start  = get_time()
        while get_time() - start < n:
            pass

    def one_maze(x, y, n):
        def exec():
            move_to(x, y)
            sleep(1)
            while True:
                move_to(x, y)
                bush(get_ctx(x, y))
                use_item(Items.Weird_Substance, n)
                step_maze()
        return exec

    
    spawn_drone(one_maze(15,15,8))
    spawn_drone(one_maze(0,15,8))
    spawn_drone(one_maze(15,0,8))
    one_maze(0,0,8)()
    

def farms():
    def subplot(x, y, fns, width):
        plots = []
        for _ in range(width):
            extend(plots, fns)
        def exec():
            move_to(x, y)
            plant_rep(plots, x, y)
        return exec

    carrots = subplot(0, 6, [carrot], 4)
    grasses = subplot(4, 6, [grass], 4)
    sunflowers = subplot(8, 6, [sunflower], 2)
    trees= subplot(10, 6, [alternate(tree, bush), alternate(bush, tree)], 3)
    pumpkins = build_pumpkin_patch(6, (0, 0))

    def drone1():
        while True:
            carrots()
            grasses()

    def drone2():
        while True:
            sunflowers()

    def drone3():
        while True:
            trees()
    
    spawn_drone(drone1)
    spawn_drone(drone2)
    spawn_drone(drone3)
    while True:
        pumpkins()
        
    # TODO: Layout engine to optimize drone movements. Since all planting assumes
    # south->north,west->east there's a lot of wasted time moving between sub-plots
    # where-as a more efficient zig-zag routine would work better. Even when traversing
    # a pumpkin patch (inbetween direct moves, like the initial planting)
    # 
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

def main():
    clear()
    move_to(0, 0)
    change_hat(Hats.Traffic_Cone_Stack)
    pet_the_piggy()
    mazes()

main()
