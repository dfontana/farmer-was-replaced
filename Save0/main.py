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
            # TODO: Should move to middle of maze, not corner!
            move_to(x, y)
            sleep(1)
            while True:
                move_to(x, y)
                bush(get_ctx(x, y))
                use_item(Items.Weird_Substance, n)
                step_maze()
        return exec

    def multi_maze():
        num_sq_per_side = (max_drones()**(1/2)) // 1
        size = WORLD_SIZE // num_sq_per_side
        for x in range(num_sq_per_side):
            for y in range(num_sq_per_side):
                spawn_drone(one_maze(x*size, y*size, size))

    # TODO run mazes

def farms():
    def subplot(x, y, fns, width):
        plots = []
        for _ in range(width):
            extend(plots, fns)
        def exec():
            move_to(x, y)
            plant_rep(plots, x, y)
        return exec

    def run(fns):
        def exec():
            while True:
                for fn in fns:
                    fn()
        return exec

    carrots = subplot(0, 6, [carrot], 4)
    grasses = subplot(4, 6, [grass], 4)
    sunflowers = subplot(8, 6, [sunflower], 2)
    trees= subplot(10, 6, [
        alternate(tree, bush),
        alternate(bush, tree)
    ], 3)
    pumpkins = build_pumpkin_patch(6, (0, 0))
    cacti = build_cacti_patch(16, (0, 0))
    run([cacti])()

    def all_trees():
        wdth = WORLD_SIZE // max_drones()
        for i in range(max_drones()):
            spawn_drone(run([
                subplot(i*wdth, 0, [
                    alternate(tree, bush),
                    alternate(bush, tree)
                ],
                wdth/2)
            ]))
    # all_trees()
    
    # spawn_drone(run([carrots, grasses]))
    # spawn_drone(run([sunflowers]))
    # spawn_drone(run([trees]))
    # while True:
    #     pumpkins()
        
def main():
    # clear()
    move_to(0, 0)
    change_hat(Hats.Traffic_Cone_Stack)
    pet_the_piggy()
    # mazes()
    farms()

main()
