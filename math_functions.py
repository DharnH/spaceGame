def hull_reduction(hull):
    if hull == 'standard metal':
        return 20
    elif hull == "hardened metal":
        return 40



    elif hull == 'almost but not quite cheater hull':
        return 90

    elif hull == 'almost cheater hull':
        return 99

    elif hull == 'cheater hull':
        return 100


'''
for i in range(1,12001):
    print()
    print('elif hull_level == ' + str(i))
    print('    return ' + str(int((i / 12000) * 100)))
'''
