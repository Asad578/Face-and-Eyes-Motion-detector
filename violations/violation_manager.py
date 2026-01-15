from config.settings import MAX_VIOLATIONS

class ViolationManager:
    def __init__(self):
        self.attempts = 0
        self.records = []

    def register(self, violation):
        self.attempts += 1
        self.records.append(violation)
        print(f"[VIOLATION {self.attempts}] {violation}")

        return self.attempts <= MAX_VIOLATIONS
