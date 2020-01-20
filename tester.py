# tester script for ESC190 lab 0
import avl_tree
from avl_tree import *
from utilities import *

def test_languages(fname):
    data = open(fname, 'r')
    print("Testing tree building")
    languages = lab0.Languages()
    data_by_year = languages.build_trees_from_file(data)
    
    for k in data_by_year.keys():
        print("Tree at year," , k, "Root?" , str(data_by_year[k].root._val) + ". Balance is:"+ str(data_by_year[k].find_balance_factor(data_by_year[k].root)) + ". Tree is balanced?:",data_by_year[k].is_balanced())
        print_paths(data_by_year[k].root)
        print()

    print()
    data.close()
   
    query = 'English'
    data_by_name = languages.query_by_name(query)

    print("The statistics for English in Canada, by year:")
    print(data_by_name)
    
    data_test = languages.query_by_count(10000)
    print(data_test)

    return data_by_year
    


def print_paths_helper(root,past, L):
    if (root.right == None and root.left == None):
        print(past + "[ " + root._val + " bf: " + str(root.bf) + " h: " + str(root.height)+ "] Length:",L)
    else:
        L+=1
        past += ("[" + root._val + " bf: " + str(root.bf) + " h: " + str(root.height)+ "] ")
        if (root.left is not None): 
           
            print_paths_helper(root.left,past,L)
        if (root.right is not None): 
         
            print_paths_helper(root.right,past,L)
    
def print_paths(root):
    print_paths_helper(root,"",0)

if __name__ == "__main__":
   
    ca_data_fname = 'data/ca_languages.csv'
    # us_data_fname = ''
    ca_data_by_year = test_languages(ca_data_fname)
    
    '''
    r = Node("f")
    tree = BalancingTree(r)
    print(tree.root._val)
    tree.balanced_insert(Node("h"))
    tree.balanced_insert(Node("y"))
    tree.balanced_insert(Node("r"))
    tree.balanced_insert(Node("z"))
    tree.balanced_insert(Node("b"))
    tree.balanced_insert(Node("a"))
    tree.balanced_insert(Node("e"))
    print_paths(tree.root)
    '''
    
    r = Node(LanguageStat("0",0,0))
    tree = BalancingTree(r)
    for i in range(1,100):
        tree.balanced_insert(Node(LanguageStat(str(i),i,i)))
    
    
    #for i in range(1,100):
        #print("is " +str(i) +" in tree? " + str(tree.search(str(i))))
            
    print_paths(tree.root)
    print("Balanced?", tree.is_balanced())
