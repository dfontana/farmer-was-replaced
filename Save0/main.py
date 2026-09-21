from utils import *
from maze import build_maze
from snake import build_snake
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

def mazes():
    # Divide world into smaller 5x5 mazes
    n = 5
    num_sq_per_side = WORLD_SIZE // n
    for x in range(num_sq_per_side):
        for y in range(num_sq_per_side):
            xp = x*n + (n // 2)
            yp = y*n + (n // 2)
            if not spawn_drone(build_maze(xp, yp, n)):
                return

def all_trees():
    for i in range(min(WORLD_SIZE, max_drones())):
        fns = []
        if i % 2 == 0:
            fns.append(alternate(fertilized(tree), bush))
        else:
            fns.append(alternate(bush, fertilized(tree)))
        spawn_drone(run([
            subplot(i, 0, fns, 1)
        ]))

def all_cacti():
    # TODO: Internally parallelized so doesn't subplot well, need limits
    run([build_cacti_patch(16, (0, 0))])()
     
def farms():
    carrots = subplot(0, 6, [carrot], 4)
    grasses = subplot(4, 6, [grass], 4)
    sunflowers = subplot(8, 6, [sunflower], 2)
    trees= subplot(10, 6, [
        alternate(tree, fertilized(bush)),
        alternate(bush, tree)
    ], 3)
    pumpkins = build_pumpkin_patch(6, (0, 0))
    
    spawn_drone(run([carrots]))
    spawn_drone(run([grasses]))
    spawn_drone(run([sunflowers]))
    spawn_drone(run([trees]))
    spawn_drone(run([pumpkins]))

def main():
    clear()
    move_to(0, 0)
    change_hat(Hats.Traffic_Cone_Stack)
    pet_the_piggy()
    mazes()
    # farms()
    # all_cacti()
    # all_trees()
    # build_snake(4)()

main()
