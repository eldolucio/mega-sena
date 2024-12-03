import random
from collections import Counter

class CombinationGenerator:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.number_weights = self._calculate_weights()
    
    def _calculate_weights(self):
        """Calculate weights for each number based on historical data"""
        freq = self.analyzer.number_frequency
        total = sum(freq.values())
        return {num: count/total for num, count in freq.items()}
    
    def generate_combinations(self, num_combinations=10):
        """Generate optimized combinations based on historical patterns"""
        combinations = []
        for _ in range(num_combinations):
            combination = self._generate_single_combination()
            combinations.append(sorted(combination))
        return combinations
    
    def _generate_single_combination(self):
        """Generate a single optimized combination"""
        numbers = list(range(1, 61))
        weights = [self.number_weights.get(num, 0) for num in numbers]
        
        # Adjust weights based on even/odd ratio
        target_even_ratio = self.analyzer._calculate_even_odd_ratio()
        
        combination = set()
        while len(combination) < 6:
            num = random.choices(numbers, weights=weights, k=1)[0]
            if num not in combination:
                current_even_ratio = len([x for x in combination if x % 2 == 0]) / len(combination) if combination else 0
                if len(combination) < 5:
                    combination.add(num)
                else:
                    # For the last number, ensure we're close to historical even/odd ratio
                    if abs((current_even_ratio + (num % 2 == 0)) / 6 - target_even_ratio) < 0.2:
                        combination.add(num)
        
        return sorted(list(combination))
    
    def calculate_combination_probability(self, combination):
        """Calculate the theoretical probability of a combination"""
        prob = 1.0
        for num in combination:
            prob *= self.number_weights.get(num, 0)
        return prob