class Calculation:
    def __init__(self):
        self.calculationLine = ""

    def SetCalculationLine(self, new_line):
        self.calculationLine = new_line

    def SetLastSymbolCalculationLine(self, symbol):
        self.calculationLine += symbol

    def GetCalculationLine(self):
        print(self.calculationLine)

    def GetLastSymbol(self):
        if self.calculationLine:
            return self.calculationLine[-1]
        return None

    def DeleteLastSymbol(self):
        if self.calculationLine:
            self.calculationLine = self.calculationLine[:-1]
        else:
            print("Строка пуста.")

calc = Calculation()

calc.SetCalculationLine("2+3")
calc.GetCalculationLine()

calc.SetLastSymbolCalculationLine("*")
calc.GetCalculationLine()

print(f"Последний символ: {calc.GetLastSymbol()}")

calc.DeleteLastSymbol()
calc.GetCalculationLine()