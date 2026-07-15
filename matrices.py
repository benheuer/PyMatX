class Matrix:

    def __init__(self,data):

        self.data = data

    def __str__(self):
        return "⌈"+"|\n|".join(" ".join(f"{element:g}" for element in row) for row in self.data)+"⌋"

    def __format__(self, spec):
        return ""⌈"+"|\n|".join(" ".join(format(element,spec) for element in row) for row in self.data)+"⌋""

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self,data):
        if len({len(row) for row in data}) != 1:
            raise ValueError("Matrix has an incorrect number of elements")
        if not data or not all(isinstance(element, (float,int)) for row in data for element in row):
            raise ValueError("Matrix data not formatted correctly")
        self._data = [[float(x) for x in row] for row in data]

    @classmethod
    def get(cls, data):
        if not data:
            raise ValueError("Missing data")
        return cls(data)

    # Matrix management below #

    def dimensions(self):
        return (len(self.data),len(self.data[0]))

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self.data)*len(self.data[0])

    def __neg__(self):
        return self * -1

    def __iter__(self):
        return iter(self.data)

    def elements(self):
        for i in range(len(self.data)):
            for k in range(len(self.data[0])):
                yield self.data[i][k]

    def __getitem__(self, index):
        if not isinstance(index,int):
            raise TypeError("Matrix indecies may only be integers.")
        return self.data[index//self.dimensions()[1]][index%self.dimensions()[1]]

    def __add__(self,other):

        if not isinstance(other, Matrix):
            raise TypeError("Matrices may only be added to other matrices")

        if self.dimensions() != other.dimensions():
            raise ValueError("Invalid dimensions")

        result = []

        for i in range(len(self.data)):
            row = []
            for j in range(len(self.data[0])):
                row.append(self.data[i][j] + other.data[i][j])
            result.append(row)
            row = []

        return Matrix(result)

    def __sub__(self,other):

        if not isinstance(other, Matrix):
            raise TypeError("Matrices may only be subtracted by other matrices")

        if self.dimensions() != other.dimensions():
            raise ValueError("Invalid dimensions")

        result = []


        for i in range(len(self.data)):
            row = []
            for j in range(len(self.data[0])):
                row.append(self.data[i][j] - other.data[i][j])
            result.append(row)
            row = []

        return Matrix(result)

    def __mul__(self, other):
        if not isinstance(other, Matrix) and not isinstance(other,(float,int)):
            raise TypeError("Matrices may only be multiplied by other matrices or a scalar")

        if isinstance(other,Matrix):
            if self.dimensions()[1] != other.dimensions()[0]:
                raise ValueError("Invalid dimensions")

            rows = self.dimensions()[0]
            cols = other.dimensions()[1]
            inner = self.dimensions()[1]

            result = []

            for i in range(rows):
                row = []
                for j in range(cols):
                    value = 0
                    for k in range(inner):
                        value += self.data[i][k] * other.data[k][j]
                    row.append(value)
                result.append(row)

        if isinstance(other,(float,int)):
            row_count = self.dimensions()[0]
            element_count = len(self.data[0])

            result = []

            for i in range(row_count):
                row = []
                for j in range(element_count):
                    value = self.data[i][j] * other
                    row.append(value)
                result.append(row)

        return Matrix(result)

    def __truediv__(self,other):

        if not isinstance(other, (Matrix, int, float)):
            raise TypeError("Matrices may only be divided by other matrices or a scalar")

        if isinstance(other, Matrix):
            if self.dimensions() != other.inverse().dimensions():
                raise ValueError("Invalid dimensions")
            return self * (other.inverse())

        else:
            return self * (1/other)

    def __pow__(self,other):

        if not isinstance(other, int):
            raise TypeError("Matrices may only be raised to a power of integers.")

        if not self.dimensions()[0] == self.dimensions()[1]:
            raise ValueError("Non-square matrices may not be raised to powers.")

        result = identity(self.dimensions()[0])

        for _ in range(other):
            result = result * self

        return result

    def inverse(self):

        error_bar = 1e-12

        if self.dimensions()[0] != self.dimensions()[1]:
            raise ValueError("Cannot invert a non-square matrix")
        else:
            size = self.dimensions()[0]

        result = identity(size)
        clone = Matrix([[x for x in row] for row in self.data])

        for i in range(size):
            if abs(clone.data[i][i]) > error_bar:
                pass
            else:
                for k in range(size-i):
                    if abs(clone.data[i+k][i]) > error_bar:
                        duplicator_clone = clone.data[i+k]
                        duplicator_res = result.data[i+k]
                        clone.data[i+k] = clone.data[i]
                        clone.data[i] = duplicator_clone
                        result.data[i+k] = result.data[i]
                        result.data[i] = duplicator_res
                        break
                    elif k == (len(self.data)-i-1):
                        raise ValueError("Singular matrices do not have inverses.")
            pivot = clone.data[i][i]
            for j in range(len(clone.data[i])):
                    result.data[i][j] = result.data[i][j]/pivot
                    clone.data[i][j] = clone.data[i][j]/pivot

            for n in range(size):
                if n == i:
                    pass
                elif abs(clone.data[n][i]) > error_bar:
                    scalar = clone.data[n][i]
                    for m in range(size):
                        clone.data[n][m] -= scalar * clone.data[i][m]
                        result.data[n][m] -= scalar * result.data[i][m]
                else:
                    pass

        return result


def identity(size):

    if not isinstance(size, int):
        raise ValueError("Matrices may only have integer dimensions.")

    result = []
    middle = []

    for i in range(size):
        for j in range(size):
            if j == i:
                middle.append(1)
            else:
                middle.append(0)
        result.append(middle)
        middle = []
    return Matrix(result)

def zero(height, width):

    if not isinstance(height, int) or not isinstance(width, int):
        raise ValueError("Matrices may only have integer dimensions.")

    result = []
    middle = []

    for i in range(height):
        for j in range(width):
            middle.append(0)
        result.append(middle)
        middle = []
    
    return Matrix(result)
