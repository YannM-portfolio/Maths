import numpy as np

def pick_and_remove(nb_list:np.ndarray):
    '''
    Input: a number list. It represents the basic list of numbers you have to choose from to solve the "Le Compte est Bon" problem.
    Output: 2 different numbers at random within the list and the remaining list (you don't replace the numbers you picked).

    The goal of this function is to choose 2 numbers at random and apply a random operation to them to obtain a new numbers.
    '''
    i1, i2 = np.random.choice(list(range(len(nb_list))), 2, replace=False)
    new_nb_list = np.delete(nb_list, (i1,i2))
    return nb_list[i1], nb_list[i2], new_nb_list

def is_operable(num1, num2, operator) -> bool:
  '''
  Input: Two positive integers and an operator of the form "+", "-", "*", or "/".
  Output: a boolean value asserting whether it is possible to obtain a positive integer using the operation "num1 operation num2".
  '''
  if operator == '+':
    return True
  elif operator == '-':
    if num1 > num2:
      return True
    return False
  elif operator == '/':
    if num1 % num2 == 0:
      return True
    return False
  elif operator == '*':
    return True
  return False

def possible_operations(num1, num2):
  '''
  Input: Two positive integers
  Output: the subset of all operators such that the operation "num1 operation num2" yields a positive integer.
  '''
  operators = ['+', '-', '/', '*']
  res = []
  for operator in operators:
    if is_operable(num1, num2, operator):
      res.append(operator)
  return res

def apply_operation(num1, num2, operator):
  '''
  Input: Two positive integers and an operator of the form "+", "-", "*", or "/".
  Output: the operation "num1 operation num2"

  Upon verifying whether num1 and num2 are operable using operator, computes the result of the above operation.
  '''
  if operator == '+':
    return num1 + num2
  elif operator == '-':
    return num1 - num2
  elif operator == '/':
    return num1 / num2
  else:
    return num1 * num2
  
def random_operations(number_list:list, nb_to_use:int):
  '''
  Input: A list of number and the number of numbers to use from it.
  Output: A random sequence of operations using "nb_to_use" numbers

  This function is the basic building block of the random model.
  You will have to run this a few amount of times to obtain a
  solution, if reachable.
  '''
  number_heap = np.random.choice(number_list, nb_to_use, replace=False)
  operations_list = []
  while len(number_heap) > 1:
    num1, num2, number_heap = pick_and_remove(number_heap)
    operators = possible_operations(num1, num2)
    operator = np.random.choice(operators)
    new_num = apply_operation(num1, num2, operator)
    number_heap = np.append(number_heap, new_num)
    operations_list.append(f"{num1} {operator} {num2} = {new_num}")
  return number_heap, operations_list

def random_crack(number_list:list, nb_to_use:int, solution:int, max_iteration=10**5):
  '''
  Input: A number list, the number of numbers to use from it, the target solution
    and the maximum number of iterations allowed to find the solution.
  Output: If reachable, the list of operations to reach the solution. If not, a 
    random sequence of operations reaching another target.
  '''
  flag = True
  nb_iter = 0
  while flag and nb_iter < max_iteration:
    nb_iter += 1

    res, operations = random_operations(number_list, nb_to_use)
    if res[0] == solution:
      flag = False
  if flag:
    print("Solution not found!")
  else:
    print(f"Solution found in {nb_iter} attempts")
  return res, operations

def reachable_target(number_list:list, nb_to_use:int, max_iteration, limit=None):
  '''
  Input: A number list, the number of numbers to use from it, the maximum iteration
    for the random algorithm, and a limit for the targets.
  Output: A list of unique target reachable by the possible operations.

  The purpose of this function is to see the concentration of reachable target using
  a given list of numbers and a certain number of numbers from it.
  '''
  nb_lists = []
  for _ in range(max_iteration):
    res, operations = random_operations(number_list, nb_to_use)
    if limit is not None:
      if res[0] >= limit:
        continue
    nb_lists.append(res[0])
  return list(set(nb_lists))

