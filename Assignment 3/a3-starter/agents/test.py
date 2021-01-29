R='R'
W='W'
state = [
        # red's home
            [],
            [R, R],
            [R, R],
            [],
            [R, R],
            [R, R],
            [R, R],
            [R, R, R, R],
            [R],
            [],
            [W],
            [W, W],
            [W],
            [],
            [],
            [],
            [],
            [W],
            # white's home
            [W, W],
            [W, W],
            [W, W],
            [W, W],
            [W],
            [W]
        ]
def f(state):
    w_dict = {1: 0, 2:0, 3:0, 4:0, 5:0, 6:0}
    r_dict = {1: 0, 2:0, 3:0, 4:0, 5:0, 6:0}
    
    
    # cross over value for checkers on the board 
    for i in range(24):
        for checker in state[i]:
            if checker == 'R':  
                if i + 1 > 6:
                    r_dict[6] = r_dict[6] + ((i  + 1) // 6 - 1)    # add crossover
                if i + 1 == 6:
                    r_dict[6] += 1                        # add # of checkers on 6 

                # outer board checkers have landed 
                # from the crossovers and have been added to the checkers already there.
                if (i + 1) % 6 != 0:                      
                    r_dict[(i + 1) % 6 ] += 1
                else:
                    r_dict[6] += 1

    
            if checker == 'W':
                j = 24 - i
                if j + 1 > 6:
                    w_dict[6] = w_dict[6] + ((j + 1) // 6 - 1)    # add crossover
                if j + 1 == 6:
                    w_dict[6] += 1                        # add # of checkers on 6 

                if (j + 1) % 6 != 0:                      
                    w_dict[(j + 1) % 6 ] += 1
                else:
                    w_dict[6] += 1

    white_pips = 0
    red_pips = 0

    print(w_dict)
    print(r_dict)

    for value in w_dict.keys():
        white_pips = white_pips + value * w_dict[value]

    for value in r_dict.keys():
        red_pips = red_pips + value * r_dict[value]
    
    # less pips, better strategy 
    print('White pips', white_pips, '\n', 'Red pips', red_pips)

f(state)
