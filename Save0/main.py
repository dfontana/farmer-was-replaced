from utils import move_to
from maze import step_maze
from plants import *

WORLD_SIZE = get_world_size()

def plant_col(fn, x, y):
    bound = WORLD_SIZE - y
    for y_p in range(bound):
        fn(get_ctx(x, y_p))
        if y_p != bound - 1:
            move(North)

def plant_rep(fn_list, x, y):
    for col_fn in fn_list:
        plant_col(col_fn, x, y)
        x += 1
        move_to(x, y)

def farm():
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

def main():
    move_to(0, 0)
    change_hat(Hats.Traffic_Cone_Stack)
    pet_the_piggy()

    while True:
        bush(get_ctx(0, 0))
        use_item(Items.Weird_Substance, WORLD_SIZE)
        step_maze()

main()
