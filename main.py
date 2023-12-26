from group import Group
from util import encrypt

MODULE_N = 1060105447831

if __name__ == "__main__":
    gr = Group(MODULE_N)
    root, x = gr.pohlig_hellman(encrypt)
    print(f"k = g^x = {root}^{x} = {pow(root, x, MODULE_N)}")
