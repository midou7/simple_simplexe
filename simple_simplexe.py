#!/usr/bin/python3
import numpy as np
np.set_printoptions(suppress=True)

from tabulate import tabulate
#np.set_printoptions(formatter={'all':lambda x: str(fractions.Fraction(x).limit_denominator())})
max_value = np.finfo(np.float64).max
def lp_cons(a,b,C,filename='file_test.lp'):
    '''
    Construct an lp file from problem vectors a,b and C
    '''
    c,n = a.shape
    xi = ['x' + str(i+1) for i in range(n)  ]
    with open(filename,'w') as f:
        f.write('Maximize\nobj: ')
    for i in range(n):
        if i != n-1:
            with open(filename,'a') as f:
                f.writelines([
                str(C[i]) + ' ' + xi[i] + ' + '
                ]
                )
        else:
            with open(filename,'a') as f:
                f.writelines([
                    str(C[i]) + ' ' + xi[i] + '\n'
                    ]
                    )
    with open(filename,'a') as f:
        f.write('Subject to\n')
    for j in range(c):
        with open(filename,'a') as f:
            f.write('c' + str(j+1) + ': ')
        
        for i in range(n):
            if i != n-1:
                with open(filename,'a') as f:
                    f.writelines([
                    str(a[j][i]) + ' ' + xi[i] + ' + '
                    ]
                    )
            else:
                with open(filename,'a') as f:
                    f.writelines([
                    str(a[j][i]) + ' ' + xi[i] + ' <= '
                    ]
                    )
        with open(filename,'a') as f:
            f.write(str(b[j])+'\n')
    with open(filename,'a') as f:
        #f.write('Generals\n')
        #for i in range(n):
            #f.write(xi[i] + ' ')
        f.write('End')    

        
            
            
    #for row in range(c):
     #   for col in range(n):

def generate_tables():
    '''
    Random simple lp problems
    '''
    n,c = np.random.randint(2,4,2)
    #with open('file_test','w') as f:
     #   f.write(str(n) + ' ' + str(c)  + '\n')
    
    #print(f'{n = },{c = }')
    e = np.eye(c)
    b = np.random.randint(1,100,c)
    C = np.zeros(n+c+1)
    for i in range(n):
        C[i] = np.random.randint(1,50)
    a = np.random.randint(1,10,(c,n))
    #print(f'{b = },{c = }, {a = }')
    Z = np.column_stack([a,e])
    #print(f'{Z = }')
    Z = np.column_stack([Z,b.T])
    #print(f'{Z = }')
    Z = np.row_stack([Z,C])
    #print(f'{Z = }')
    #with open('file_test','a') as f:
    header = str(n) + ' ' +  str(c)
    np.savetxt('file_test',Z,fmt='%g',header=header,comments='')
    lp_cons(a,b,C)
    return Z
def sol_output(tab,tab_name,fileout=False):
    rows,cols = tab.shape
    n_dec = cols - rows -1
    xs = ['$x_' + str(i+1) + '$' for i in range(n_dec)]
    ss = ['$s_' + str(i+1) + '$' for i in range(rows-1)]
    header = xs + ss + ['$b_i$']
    print(tab_name)
    tab_l = tab[:,0:cols-1]
    zs = [''] * (len(tab_l) - 1) + ['$Z$']
    #print(zs)
    tab_l = np.column_stack([zs,tab_l])
    #tab_ll = np.column_stack([zs,tab_l])
    #print(tab_ll)
    print(tabulate(tab_l,headers=header,tablefmt='pretty'))
    if tab_name.endswith('ial') and fileout:
        with open('sol_output.tex','w') as f:
            f.write('\n' + tab_name + '\n')
            f.write(tabulate(tab_l,headers=header,tablefmt='latex'))
    elif fileout:
        with open('sol_output.tex','a') as f:
            f.write('\n' + tab_name + '\n')
            f.write(tabulate(tab_l,headers=header,tablefmt='latex'))
def sol_output_glob(tables):
    '''Print or export simplexe tables '''
    #print(f'{len(tables) = }')
    rows,cols = tables[0].shape
    #print(f'{tab.shape = }')
    n_dec = cols - rows -1
    xs = ['$x_' + str(i+1) + '$' for i in range(n_dec)]
    ss = ['$s_' + str(i+1) + '$' for i in range(rows-1)]
    header = xs + ss + ['$b_i$']
    tab = tables[0]
    print(tabulate(tab[:,0:cols-1],headers=header,tablefmt='github'))
    with open('sol_output.tex','w') as f:
        f.write('Tableau initial :\\\\\n')
        f.write(tabulate(tab[:,0:cols-1],headers=header,tablefmt='latex_raw'))
    tables.pop(0)
    #print(f'{len(tables) = }')
    for idx,tab in enumerate(tables):
        print(tabulate(tab[:,0:cols-1],headers=header,tablefmt='github'))
        with open('sol_output.tex','a') as f:
            if idx < len(tables) - 1 :
                f.write('\n\\\\Tableau ' + str(idx+1) + ' :\\\\\n')
                f.write(tabulate(tab[:,0:cols-1],headers=header,tablefmt='latex_raw'))
            else:
                f.write('\n\\\\Tableau final :\\\\\n')
                f.write(tabulate(tab[:,0:cols-1],headers=header,tablefmt='latex_raw'))
def latex_table_print(tab):
    rows,cols = tab.shape
    #print(f'{tab.shape = }')
    n_dec = cols - rows -1
    xs = ['x_'+str(i+1) for i in range(n_dec)]
    ss = ['s_'+str(i+1) for i in range(rows-1)]
    header = xs + ss + ['b_i']
    print(tabulate(tab[:,0:cols-1],headers=header,tablefmt='latex'))

def simplexe(tab):
    '''
    this is a simple simplexe method to solve a normal canonic maximisation problem
    tab is the first table of the well known simplexe algorithm.
    '''
    print(f'{tab = }  ')
    #print(f'{np.argmax(tab[-1]) = }')
    #print(f'{np.max(tab[-1]) = }')
    #tables = []
    rows,cols = tab.shape
    #print(f'{xs = }')
    #print(f'{ss = }')
    rate = np.zeros(rows)
    #print(f'{rate.T.shape =}')
    tab = np.c_[tab,rate]
    sol_output(tab,'Tableau initial')
    #sol_output(tab,'Tableau initial',True)
    tour = 0
    while any(elt > 1e-7 for elt in tab[-1,:]):
        argmax = np.argmax(tab[-1])
        for i in range(rows-1):
            tab[i][cols] = tab[i][cols-1] / tab[i][argmax] if tab[i][argmax] != 0 else max_value
            #print(f'{tab[i,cols] = }')
        argmin = np.argmin(tab[0:rows-1,cols])
        #print(argmin)
        rang = [i for i in range(rows) if i != argmin]
        #rang_c = [j for j in range(cols) if j!= argmax]
        #print(f'{rang = }')
        #print(f'{rang_c = }')
        for i in rang:
            facteur =  tab[i,argmax] / tab[argmin,argmax]
            #print(f'{facteur =}')
            for j in range(cols):
                tab[i,j] -= facteur * tab[argmin,j]
        tour += 1
        sol_output(tab,'Tableau ' + str(tour))
        #sol_output(tab,'Tableau ' + str(tour),True)
        if tour == 50:
            break
        
        
    
def read_file(filename='file_d'):
    '''
    this is a file example: 
        2 2 
        1 1 1 0 1000
        15 3 0 1 4500
        8 4 0 0 0
    which is the following maximisation problem:
    max 8x + 4y
    st  
        x + y    <= 1000
        15x + 3y <= 4500
        x,y >= 0
    '''
    with open(filename,'r') as f:
        n,c = map(int,f.readline().split(' '))
        #print(f'{type(n) = }')
        a = np.zeros((c,n))
        b = np.zeros(c)
        C = np.zeros(n)
        for i in range(c):
            line = f.readline()
            #m = len(line.split(' '))
            #print(f'{m = }')
            for j in range(n):
                a[i][j] = float(line.split(' ')[j])
            
            b[i] = float(line.split(' ')[-1])
        line = f.readline()
        for i in range(n):
            C[i] = float(line.split(' ')[i])
    e = np.eye(c)
    
    z = np.zeros(n+c+1)
    z[0:n] = C
    Z = np.column_stack([a,e,b])
    Z = np.row_stack([Z,z])
    # print(f'{a = }')
    # print(f'{b = }')
    # print(f'{C = }')
    lp_cons(a,b,C,f'{filename}.lp')
    return Z
        



def main(filename='test'):
    Z = []
    #print(f'{filename =}')
    with open(filename) as f:
        line = f.readline()
        _,ncons = map(int,line.split(' '))
        for _ in range(ncons+1):
            line = f.readline()
            elt = [float(x) for x in line.split(' ')]
            Z.append(elt)
    Z = np.array(Z,np.float64)
    
    
    # #dic = {'Z':Z,'C':C}
    #print(f'{Z =}')
    simplexe(Z)

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        #main(filename)
        Z = read_file(filename)
        simplexe(Z)
    else:
        #main()
        Z = generate_tables()
        simplexe(Z)
        #Z = read_file()
        #simplexe(Z)
        
