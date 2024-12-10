from typing import List

class AverageStrategy:
    def calculate(self, data: List[float]) -> float:
        raise NotImplementedError("Метод должен быть переопределен в подклассе.")

class ArithmeticMean(AverageStrategy):
    def calculate(self, data: List[float]) -> float:
        return sum(data) / len(data) if data else 0

class GeometricMean(AverageStrategy):
    def calculate(self, data: List[float]) -> float:
        product = 1
        for x in data: product *= x
        return product**(1 / len(data)) if data else 0

class HarmonicMean(AverageStrategy):
    def calculate(self, data: List[float]) -> float:
        return len(data) / sum(1 / x for x in data) if data and all(x != 0 for x in data) else 0

class AverageContext:
    def __init__(self, strategy: AverageStrategy): self.strategy = strategy
    def set_strategy(self, strategy: AverageStrategy): self.strategy = strategy
    def execute(self, data: List[float]) -> float: return self.strategy.calculate(data)

data = [2, 4, 6, 8, 10]
strategies = [ArithmeticMean(), GeometricMean(), HarmonicMean()]
results = []

for strategy in strategies:
    context = AverageContext(strategy)
    result = context.execute(data)
    results.append(result)
    print(f"Результат стратегии {strategy.__class__.__name__}: {result:.2f}")

print(f"Максимальное значение: {max(results):.2f}")
print(f"Минимальное значение: {min(results):.2f}")