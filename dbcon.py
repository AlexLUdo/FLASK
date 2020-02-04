import sqlite3

def put(vacancy,area_query,vse_skily,all_found_vac):
    skl = list({name: dict.keys for name in dict.keys(vse_skily)})
    skl = str(skl)
    print(skl)
    print(type(skl))
    conn = sqlite3.connect('xx.sqlite', check_same_thread=False)
    cur = conn.cursor()
    cur.execute("INSERT INTO zapros (vac,reg,num) VALUES(?,?,?)", (vacancy, area_query, all_found_vac))
    cur.execute("INSERT INTO skills (skl,reg) VALUES(?,?)", (skl, area_query))
    conn.commit()
    conn.close()


def get(area):
    conn = sqlite3.connect('xx.sqlite', check_same_thread=False)
    cur = conn.cursor()
    cur.execute('SELECT * from zapros where reg=?', (area,))
    print(cur.fetchall())
    result = cur.fetchall()
    print(result)
    print(type(result))
    conn.close()
    return result
