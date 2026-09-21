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

def all_pumpkins():
    # Divide the world into 6x6 squares with 1 space between each
    n = 6
    num_sq_per_side = (WORLD_SIZE+1) // (n+1)
    for x in range(num_sq_per_side):
        for y in range(num_sq_per_side):
            xp = x*(n+1)
            yp = y*(n+1)
            if not spawn_drone(run([build_pumpkin_patch(n, (xp, yp))])):
                return

def all_cacti():
    # TODO: Internally parallelized so doesn't subplot well, need limits
    run([build_cacti_patch(16, (0, 0))])()
     
def farms():
    set_world_size(22)
    all_pumpkins()
    # TODO: Could use horizontal plots (movement is left->right)
    # TODO: Nice to have: bound the plot upper right corner

    # TODO: Polyculture combinator -- it's always a diff plant and it's
    #       grass|bush|tree|carrot so it's very easy to do this
    #       but the major gotcha is the (x,y) part that it wants -- simple
    #       alternation won't work. It may be more intersting to create
    #       a bounded plot of just polycultures as a result
    # Carrots feed pumpkins
    spawn_drone(run([subplot(6, 0, [carrot], 1)]))
    spawn_drone(run([subplot(13, 0, [carrot], 1)]))
    spawn_drone(run([subplot(21, 0, [carrot], 1)]))

    # Grass & Tree feed carrot
    spawn_drone(run([subplot(0, 20, [grass], 6)]))
    spawn_drone(run([subplot(7, 20, [
        alternate(tree, bush),
        alternate(bush, tree)
    ], 3)]))
    spawn_drone(run([subplot(20, 0, [
        alternate(tree, bush),
    ], 1)]))
    spawn_drone(run([subplot(14, 20, [
        alternate(tree, bush),
        alternate(bush, tree)
    ], 3)]))

def main():
    # clear()
    move_to(0, 0)
    change_hat(Hats.Traffic_Cone_Stack)
    pet_the_piggy()
    # mazes()
    farms()
    # all_cacti()
    # all_trees()
    # build_snake(4)()

main()
