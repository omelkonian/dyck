from ..dyck import Grammar
from ..grammar_utils import *

################################################################################
########################### TOO POWERFULL TO HANDLE  ###########################
# mcfg3 = Grammar([
#     r('S <- W', {(x, y, z)}),
#     O('W <- W, W', {(x, y, z), (l, m, n)}, x=l, y=m, z=n),
#     r('$W <- W', {(x, '$', y, '$', z)}),
# ])
################################################################################

# NB: remarkable performance with 102 rules
#
# Completeness:
# - n4 yes
# - n5 yes
# - n6 yes
# - n7 ?
# - n8 ?
#
# Stress:
# - n2 yes
# - n3 yes
# - n4 no (aa$bb$acbaccbc)
# - n5 no (aa$bb$acbaccbcabc)
# - n6 no (aa$bb$acbaccbcabcabc)
# - n7 no (aa$bb$acbaccbcabcabcabc)
#
def non_deleting_interleaving(o):
  """ no empty tuple element (ie. utilize commas maximally)
  PRO TIP: When running, listen to 'Charlemagne Palestine - Strumming Music'
  """
  return all([len(x) > 0 for x in o])

def non_deleting_interleaving2(o):
  """ no empty tuple element (ie. utilize commas maximally)
  PRO TIP: When running, listen to 'Charlemagne Palestine - Strumming Music'
  """
  return (all([len(x) > 0 for x in o]) and
          x in o[0] and y in o[1] and z in o[2])

# NB: fails miserably
def equal_interleaving(o):
  """ at least two insertions in every tuple element """
  return all([len(x) == 2 for x in o])

mcfg3 = Grammar([
    ('S', ['W'], [(x, y, z)]),

    # -- Strict base
    ('W', [], [[a],[b],[c]]),

    # -- Flexile base
    # O('W', {(a, b, c)}, splits=2),

    # -- Covered by interleaving in the 3-MCFG case
    # C('W <- W', {(a, x, b, y, c, z)},
    #   predicate=lambda o: all([x in o[0], y in o[1], z in o[2]])),

    # -- Interleaving
    C('W <- W, W',
      orders={(x, y, z), (l, m, n)},
      predicate=non_deleting_interleaving,
      x=l, y=m, z=n),

    # -- Debugging
    r('$W <- W', {(x, '$', y, '$', z)}),
])
