'''import fire
from random import choices

def fruit_generator(fruit):
   #returns back random fruit
    fruits = ["apple", "banana", "cherry", "peach", "orange"]
    fruits.append(fruit)
    print(f"You added this fruit {fruit}")
    print(f"Randomly selected from all fruits: {fruits}")
    return choices(fruits)

#print(fruit_generator(["apple", "banana", "orange"]))

if __name__ == '__main__':
    fire.Fire(fruit_generator)
'''