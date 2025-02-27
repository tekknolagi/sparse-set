import dataclasses
import unittest

# https://research.swtch.com/sparse

@dataclasses.dataclass
class SparseSet:
    sparse: list[int] = dataclasses.field(default_factory=list)
    dense: list[int] = dataclasses.field(default_factory=list)
    n: int = 0

    def add(self, i: int) -> None:
        self.dense.append(i)
        if i >= len(self.sparse):
            self.sparse.extend([None]*(i - len(self.sparse) + 1))
        self.sparse[i] = self.n
        self.n += 1

    def __contains__(self, i: int) -> bool:
        return i < len(self.sparse) and self.sparse[i] < self.n and self.dense[self.sparse[i]] == i

    def clear(self) -> None:
        self.n = 0

class SetTests(unittest.TestCase):
    def test_init(self):
        result = SparseSet()
        self.assertEqual(result.sparse, [])
        self.assertEqual(result.dense, [])
        self.assertEqual(result.n, 0)

    def test_add(self):
        result = SparseSet()
        result.add(3)
        result.add(4)
        self.assertEqual(result.sparse, [None, None, None, 0, 1])
        self.assertEqual(result.dense, [3, 4])

    def test_contains(self):
        result = SparseSet()
        self.assertNotIn(3, result)
        result.add(3)
        self.assertIn(3, result)
        self.assertNotIn(4, result)
        result.add(4)
        self.assertIn(4, result)

    def test_clear(self):
        result = SparseSet()
        result.add(3)
        self.assertIn(3, result)
        result.clear()
        self.assertNotIn(3, result)

if __name__ == "__main__":
    unittest.main()
