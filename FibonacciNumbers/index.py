def fibonacci_sequence(n):
    if n <= 0:
        print("Введите положительное целое число.")
        return
    a, b = 1, 1
    for i in range(1, n + 1):
        print(f"{i} {a}")
        a, b = b, a + b

try:
    num = int(input("Введите количество элементов последовательности: "))
    fibonacci_sequence(num)
except ValueError: print("Пожалуйста, введите целое число.")