"""File for containing all games sprites"""


def convert(sprite):
    pos_list = [[j, i] for i, x in enumerate(sprite) for j, item in enumerate(x) if item == 'x']
    return pos_list


def convert_all(_list):
    return list(map(convert, _list))


# ------------------- ARKANOID ---------------------
ENEMIES_SMALL = convert_all([
    [' xxx ',
     'xx xx',
     'x x x',
     'xx xx',
     'xxxxx',
     'x x x',
     'x x x'],

    [' xxx ',
     'x   x',
     'x   x',
     'xxxxx',
     ' x x '],

    [' x x ',
     '  x  ',
     'xxxxx',
     ' xxx ',
     '  x  '],

    [' x   x ',
     '  x x  ',
     ' xxxxx ',
     'xxxxxxx',
     'x  x  x',
     'x  x  x',
     '   x   '],

    ['xx xx',
     'xxxxx',
     ' xxx ',
     'xxxxx',
     'xx xx',
     ' x x '],

    [' xxxxxx ',
     '  x  x  ',
     '   xx   ',
     'xxxxxxxx',
     ' xxxxxx ',
     '   xx   ',
     '   xx   '],

    ['  xxx  ',
     '   x   ',
     '  xxx  ',
     ' xxxxx ',
     'xxxxxxx',
     ' x x x ',
     '   x   '],

    ['  x  ',
     ' x x ',
     'xxxxx',
     ' x x '],

    ['xxx',
     'xxx',
     ' x ',
     ' x ']
])

ENEMIES_BIG = convert_all([
    ['    x    x    ',
     '   xxx  xxx   ',
     '    x    x    ',
     '    xxxxxx    ',
     '  xxx xx xxx  ',
     '  xxx    xxx  ',
     ' xxxxxxxxxxxx ',
     ' xx x x x x x ',
     'xxx x x x x xx',
     'xxxxxxxxxxxxxx',
     'xxxxxxxxxxxxxx',
     ' xxxx    xxxx ',
     '  xx      xx  ',
     '   x      x   '],

    ['    xxxxx    ',
     ' x xx x xx x ',
     '  xxx x xxx  ',
     ' xxxx x xxxx ',
     'xxxxxxxxxxxxx',
     'x   x x x   x',
     'xxxxxxxxxxxxx',
     'x   x x x   x',
     'xxxxxxxxxxxxx',
     ' xxxx x xxxx ',
     '  xxx x xxx  ',
     ' x xx x xx x ',
     '    xxxxx    '],

    ['      xx      ',
     '    xxxxxx    ',
     '  xx  xx  xx  ',
     '  xxx xx xxx  ',
     ' x xxx  xxx x ',
     ' x  xxxxxx  x ',
     'xxxx xxxx xxxx',
     'xxxx xxxx xxxx',
     ' x  xxxxxx  x ',
     ' x xxx  xxx x ',
     '  xxx xx xxx  ',
     '  xx  xx  xx  ',
     '    xxxxxx    ',
     '      xx      '],

    ['    xxxxxx    ',
     '  xxxxxxxxxx  ',
     ' xxxxxxxxxxxx ',
     ' xxx x  x xxx ',
     'xxx        xxx',
     'xxx   xx   xxx',
     'xxxxxxxxxxxxxx',
     'xxxxxxxxxxxxxx',
     'xxxxxxxxxxxxxx',
     '  x x x  x x  ',
     '  x x x  x x  ',
     '  x x x  x x  ',
     ' x  x  x x  x ',
     ' x  x  x x  x '],

    ['    x    x    ',
     '    x    x    ',
     '  xxxx  xxxx  ',
     ' xxxxxxxxxxxx ',
     ' xxxxxxxxxxxx ',
     ' xxxxxxxxxxxx ',
     ' xxx xxxx xxx ',
     ' xxx  xx  xxx ',
     'xxxxxxxxxxxxxx',
     'xxxxxxxxxxxxxx',
     'xxxxx    xxxxx',
     ' xx xxxxxx xx ',
     ' xx xxxxxx xx ',
     '  x        x  '],
])

SHIP_1 = convert([
 ' x ',
 'xxx'
])

SHIP_2 = convert([
 ' x ',
 ' x ',
 'xxx',
 'x x'
])

SHIP_3 = convert([
 ' x x ',
 ' x x ',
 'xxxxx',
 'x   x'
])

PROJECTILE_1 = convert([
 'x',
 'x'
])

PROJECTILE_2 = convert([
 'x',
 'x',
 'x',
 'x'
])

PROJECTILE_3 = convert([
 'x x',
 'x x',
 'x x'
])

# ------------------- RACING ---------------------
CAR = convert([
 ' x ',
 'xxx',
 ' x ',
 'xxx',
])

CAR_REVERT = convert([
 'xxx',
 ' x ',
 'xxx',
 ' x '
])

BIG_CAR = convert([
 ' x ',
 'xxx',
 'xxx',
 ' x ',
 'xxx',
 'xxx'
])

LINE = convert([
 'x',
 'x',
 ' ',
 ' '
] * 8)
