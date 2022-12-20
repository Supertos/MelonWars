
m_x = 0
m_y = 0

key_map = {}
def int_SetMousePos( x, y ):
    global m_x
    global m_y
    m_x = x
    m_y = y

def int_setKey( key, on ):
    global key_map
    key_map[ key ] = on

def isKeyPressed( key ):
    global key_map
    if key_map.get(key) is not None:
        return key_map[ key ]
    else:
        return False
def getMousePos():
    global m_x
    global m_y
    return (m_x, m_y)
