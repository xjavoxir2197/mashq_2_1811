class BankAccount:
    """Bank hisob raqami uchun asosiy klass (superklass)."""
    def __init__(self, owner, initial_balance=0.0):
        self._owner = owner  # Egasi o'zgaruvchisi
        self.__balance = initial_balance  # Balansni maxfiy saqlash (Inkapsulyatsiya)

    def deposit(self, amount):
        """Hisobga pul qo'yish."""
        if amount > 0:
            self.__balance += amount
            print(f"✅ {amount} qo'shildi. Yangi balans: {self.get_balance()} so'm.")
            return True
        return False

    def withdraw(self, amount):
        """Hisobdan pul yechish (subklasslar tomonidan qayta yoziladi - Polimorfizm)."""
        if self.__balance >= amount:
            self.__balance -= amount
            print(f"✅ {amount} yechildi. Yangi balans: {self.get_balance()} so'm.")
            return True
        else:
            print("❌ Balans yetarli emas.")
            return False

    def get_balance(self):
        """Maxfiy balansni ko'rsatish metodi."""
        return self.__balance

    def get_owner(self):
        """Hisob egasini qaytarish."""
        return self._owner

    # Maxfiy o'zgaruvchiga tashqaridan to'g'ridan-to'g'ri o'zgartirishni oldini olish
    # uchun maxsus setter yaratilmadi.

class SavingsAccount(BankAccount):
    """Jamg'arma hisob raqami (foiz qo'shish qoidasi)."""
    def __init__(self, owner, initial_balance=0.0, interest_rate=0.01):
        super().__init__(owner, initial_balance)
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        """Jamg'arma hisobidan pul yechish (foizlar bilan)."""
        # Oddiylik uchun foizni faqat yechishda hisoblaymiz
        interest = self.get_balance() * self.interest_rate
        print(f"➕ Jamg'arma foizi hisoblandi: {interest:.2f} so'm.")
        self.deposit(interest) # Foizni qo'shamiz

        # Asosiy BankAccount withdraw metodini chaqirish
        return super().withdraw(amount)

class CheckingAccount(BankAccount):
    """Hozirgi hisob raqami (overdraft imkoniyati)."""
    def __init__(self, owner, initial_balance=0.0, overdraft_limit=500.0):
        super().__init__(owner, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        """Hozirgi hisobdan pul yechish (overdraft ruxsati bilan)."""
        max_withdrawal = self.get_balance() + self.overdraft_limit

        if amount <= max_withdrawal:
            # Balans o'zgarmaydi, to'g'ridan-to'g'ri maxfiy __balance ga ta'sir qilish uchun
            # BankAccount ichidagi o'zgaruvchini o'zgartiramiz
            current_balance = self.get_balance()
            if current_balance >= amount:
                 print(f"✅ {amount} yechildi. Yangi balans: {current_balance - amount} so'm.")
            else:
                 overdraft_used = amount - current_balance
                 print(f"⚠️ {amount} yechildi (Overdraft ishlatildi: {overdraft_used} so'm). Yangi balans: {current_balance - amount} so'm.")
            
            # _BankAccount__balance orqali maxfiy o'zgaruvchini yangilash
            setattr(self, '_BankAccount__balance', current_balance - amount)
            return True
        else:
            print(f"❌ Yechish mumkin emas. Limit: {max_withdrawal} so'm.")
            return False


# --- Polimorfik foydalanish ---
print("--- Bank Hisoblarida Polimorfizm ---")
accounts = [
    SavingsAccount("Ali", 1000, 0.05),
    CheckingAccount("Vali", 500, 100)
]

# Bitta ro'yxatda turli hisoblarni saqlab, bir xil buyruq (withdraw) beramiz
for account in accounts:
    print(f"\n👤 {account.get_owner()} hisobi (Turi: {type(account).__name__})")
    print(f"💳 Boshlang'ich balans: {account.get_balance()} so'm")

    # Polimorfizm: Har bir klass o'zining withdraw() metodini chaqiradi
    if account.withdraw(100):
        print(f"💰 Qoldiq: {account.get_balance()} so'm")

# CheckingAccount'da overdraftni sinash
print("\n--- Overdraftni sinash (CheckingAccount) ---")
accounts[1].withdraw(550) # Balans 400, limit 100 => 500 ga qadar ruxsat. 550 rad etiladi.
accounts[1].withdraw(500) # Balans 400, limit 100 => 500 ga qadar ruxsat. 500 yechiladi.
