from utils import *
from maze import build_maze
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
    # Divide world into smaller 5x5 mazes
    n = 5
    num_sq_per_side = WORLD_SIZE // n
    for x in range(num_sq_per_side):
        for y in range(num_sq_per_side):
            xp = x*n + (n // 2)
            yp = y*n + (n // 2)
            # TODO: Should move to middle of maze, not corner!
            if not spawn_drone(build_maze(xp, yp, n)):
                return

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
    # run([cacti])()

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
    all_trees()
    
    # spawn_drone(run([carrots, grasses]))
    # spawn_drone(run([sunflowers]))
    # spawn_drone(run([trees]))
    # while True:
    #     pumpkins()

def main():
    clear()
    move_to(0, 0)
    change_hat(Hats.Traffic_Cone_Stack)
    pet_the_piggy()
    mazes()
    # farms()

main()
