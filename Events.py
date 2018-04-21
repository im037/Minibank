from collections import namedtuple

BankAccountCreated = namedtuple('BankAccountCreated', ['id', 'owner'])

DepositPerformed = namedtuple('DepositPerformed', ['id', 'amount'])

OwnerChanged = namedtuple('OwnerChanged', ['id', 'new_owner'])

WithDrawalPerformed = namedtuple('WithDrawalPerformed', ['id', 'amount'])

class MutationMixi:
    def __init__(self, events=None):
        if events is not None:
            events_iterator(events)

    def events_iterator(self, events):
        for event in events:
            self.mutate(event)

    def mutate(self, event):
        method_name = f'when_{event.__class__.__name__.lower()}'
        method = getattr(self, method_name)
        method(event)


class BankAccountState(MutationMixi):
    def when_bankaccountcreated(self, event):
        self.id = event.id
        self.owner = event.owner
        self.balance = 0
    
    def when_depositperformed(self, event):
        self.balance += event.amount

    def when_ownerchange(self, event):
        self.balance -= event.amount

    def when_withdrawlperformed(self, event):
        self.owner = event.owner

class ChangesMixin(MutationMixi):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chenges = []

    def apply(self, event):
        self.changes.append(event)
        self.mutate(event)


class BankAccount(BankAccountState, ChangesMixin):
    def open_account(self, owner):
        self.apply(BankAccountCreated(
            id = uuid4(),
            owner = owner,
        ))
    
    def deposit(self, amount):
        self.apply(DepositPerformed(
            id = self.id,
            amount = amount,
        ))

    def change_owner(self, new_owner):
        self.apply(OwnerChanged(
            id = self.id,
            new_owner = new_owner,
        ))

    def withdraw(self, amount):
        if self.balance - amount < 0:
            raise ValueError(f"'{amount}' is not available")

        self.apply(WithDrawalPerformed(
            id = self.id,
            amount = amount,
        ))