import sys

# I just really felt like writing a lexer (or atleast something that kind of is a little bit similar to a lexer),
# so I just quickly wrote this math 'parser' in like 30 minutes. This is just me playing around with python and ImportError
# am aware of the low quality of this code. 

DIGITS = '0123456789'
DECIMAL_SEP = '.'
IGNORE = ' \t'
BINARY_OPERATORS = '+-*/%'
BRACES_OPEN = '('
BRACES_CLOSE = ')'

if len(sys.argv) > 1:
    input = sys.argv[1]
else:
    print('Input expected')
    exit(1)

def loop():
    pos = 0
    operation = []
    res = None
    numFlag = False
    biOpFlag = False
    numOpenBraces = 0
    posOuterBraces = None
    while pos in range(0, len(input)):
        char = input[pos]
        if char in IGNORE:
            pass
        elif char in DIGITS:
            ret = evaluateNumber(pos)
            if not numFlag:
                operation.append(str(ret[0]))
                numFlag = True
                if biOpFlag:
                    biOpFlag = False
            else:
                exitUnexpected(f'number \'{ret[0]}\'', pos)
            pos = ret[1]
        elif char in BINARY_OPERATORS:
            if numFlag and not biOpFlag:
                operation.append(char)
                biOpFlag = True
                numFlag = False
            else:
                exitUnexpected(f'operator \'{char}\'', pos)
        elif char in BRACES_OPEN:
            if numFlag:
                exitUnexpected(f'opening braces', pos)
            elif biOpFlag:
                biOpFlag = False
            if not posOuterBraces:
                posOuterBraces = pos
            operation.append(char)
            numOpenBraces += 1
        elif char in BRACES_CLOSE:
            if 0 < numOpenBraces and numFlag:
                operation.append(char)
                numOpenBraces -= 1
                if 0 == numOpenBraces:
                    posOuterBraces = None
            else:
                exitUnexpected('closing braces', pos)
        else:
            exitUnexpected(f'character \'{char}\'', pos)
        pos += 1
    if 0 < numOpenBraces:
        printPosArrow(posOuterBraces)
        print(f'Braces opened but never closed')
        exit(1)
    if biOpFlag:
        exitUnexpected('end of expression', pos)
    opString = ''.join(operation)
    res = eval(opString)
    print(f'{opString} = {res}')

def evaluateNumber(pos: int):
    num = []
    char = input[pos]
    hasSep = False
    for pos in range(pos, len(input)):
        char = input[pos]
        if char in DECIMAL_SEP:
            if hasSep:
                exitUnexpected(f'decimal seperator \'{char}\'', pos)
            else:
                hasSep = True
                num.append(char)
        elif char in DIGITS:
            num.append(char)
        else:
            break
        pos += 1
    pos -= 1 #hacky asf
    return ''.join(num), pos

def printPosArrow(pos: int) -> str:
    print(input)
    print(' '*(pos) + '^')

def exitUnexpected(itm:str, pos: int):
    printPosArrow(pos)
    print(f'Unexpected {itm}')
    exit(1)

if __name__ == '__main__':
    loop()