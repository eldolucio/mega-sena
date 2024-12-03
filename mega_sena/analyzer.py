from collections import Counter, defaultdict
from itertools import combinations

class MegaSenaAnalyzer:
    def __init__(self, historical_data):
        self.historical_data = historical_data
        self.number_frequency = self._calculate_number_frequency()
        self.pair_frequency = self._calculate_pair_frequency()
        
    def _calculate_number_frequency(self):
        """Calculate the frequency of each number"""
        all_numbers = []
        for draw in self.historical_data:
            all_numbers.extend(draw['numbers'])
        return Counter(all_numbers)
    
    def _calculate_pair_frequency(self):
        """Calculate frequency of number pairs"""
        pair_counts = defaultdict(int)
        for draw in self.historical_data:
            for pair in combinations(draw['numbers'], 2):
                pair_counts[pair] += 1
        return pair_counts
    
    def get_number_stats(self):
        """Get comprehensive statistics about number occurrences"""
        stats = {
            'frequency': dict(self.number_frequency),
            'even_odd_ratio': self._calculate_even_odd_ratio(),
            'decade_distribution': self._calculate_decade_distribution(),
            'average_intervals': self._calculate_average_intervals()
        }
        return stats
    
    def _calculate_even_odd_ratio(self):
        """Calculate the ratio of even to odd numbers"""
        even_count = sum(1 for num in self.number_frequency.elements() if num % 2 == 0)
        total_count = sum(self.number_frequency.values())
        return even_count / total_count if total_count > 0 else 0
    
    def _calculate_decade_distribution(self):
        """Calculate distribution across decades (1-10, 11-20, etc.)"""
        decades = defaultdict(int)
        for num, freq in self.number_frequency.items():
            decade = (num - 1) // 10
            decades[decade] += freq
        return dict(decades)
    
    def _calculate_average_intervals(self):
        """Calculate average interval between appearances for each number"""
        intervals = {}
        for num in range(1, 61):
            appearances = []
            last_seen = None
            for i, draw in enumerate(self.historical_data):
                if num in draw['numbers']:
                    if last_seen is not None:
                        intervals.setdefault(num, []).append(i - last_seen)
                    last_seen = i
            if intervals.get(num):
                intervals[num] = sum(intervals[num]) / len(intervals[num])
            else:
                intervals[num] = 0
        return intervals