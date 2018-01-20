# Usage
```bash
> python dyck.py -h
usage: dyck.py [-h] [-n [N]] [-w [W]] [-ws [WS]] [-p [P]] [-minp [MINP]]
               [-ps [PS]] [-g [G]] [-i [I]] [--rules] [--serialize] [--check]
               [--gen] [--range RANGE] [--time] [--rand]

Check your D3 grammar.

optional arguments:
  -h, --help     show this help message and exit
  -n [N]         number of "abc" occurences
  -w [W]         single word to check
  -ws [WS]       file containing words to check
  -p [P]         single parse of a word
  -minp [MINP]   show minimal parse of a word
  -ps [PS]       multiple parses of a word
  -g [G]         grammar to use
  -i [I]         initial symbol to use
  --rules        print all rules
  --serialize    serialize grammar to file
  --check        check soundness
  --gen          generate dyck words
  --range RANGE  search in given percentage range
  --time         measure execution time
  --rand         generate random Dyck word
```
