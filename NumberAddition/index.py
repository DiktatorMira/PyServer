def GetPositivNumber(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0: return value
            else: print("Значение должно быть положительным.")
        except ValueError: print("Пожалуйста, введите действительное значение.")

def main():
    x = GetPositivNumber("Введите x: ")
    y = GetPositivNumber("Введите y: ")
    print(f"{x}+{y}={x + y}")

if __name__ == "__main__": main()