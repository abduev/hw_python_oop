import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_record):
        self.records.append(new_record)

    def get_today_stats(self):
        return sum(i.amount for i in self.records
                   if i.date == dt.datetime.now().date())

    def get_week_stats(self):
        week_last = dt.date.today() - dt.timedelta(days=7)
        return sum(x.amount for x in self.records
                   if ((dt.datetime.now().date() >= x.date) and
                       (x.date > week_last)))


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = date
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0

    def get_today_cash_remained(self, currency):
        self.currency = currency
        cash_spent = self.get_today_stats()
        currency_dict = {'rub': (1, 'руб'),
                         'usd': (self.USD_RATE, 'USD'),
                         'eur': (self.EURO_RATE, 'Euro')
                         }
        cash_remained = round(self.limit/currency_dict[currency][0] -
                              cash_spent/currency_dict[currency][0], 2)
        if cash_remained == 0:
            return f"Денег нет, держись"
        elif cash_remained > 0:
            return ("На сегодня осталось "
                    f"{cash_remained} {currency_dict[currency][1]}")
        return ("Денег нет, держись: твой долг "
                f"- {abs(cash_remained)} {currency_dict[currency][1]}")


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_eaten = self.get_today_stats()
        calories_available = self.limit - calories_eaten
        if calories_available > 0:
            return ("Сегодня можно съесть что-нибудь ещё, но с общей "
                    f"калорийностью не более {calories_available} кКал")
        return f"Хватит есть!"
