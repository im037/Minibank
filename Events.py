from collections import namedtuple

BankAccountCreated = namedtuple('BankAccountCreated', ['id', 'owner'])

DepositPerformed = namedtuple('DepositPerformed', ['id', 'amount'])

OwnerChange = namedtuple('OwerChange', ['id', 'new_owner'])

WithDrawalPerformed = namedtuple('WithDrawalPerformed', ['id', 'amount'])

class MutationMixi:
    def __init__(self, events=None):
        if events is not None:
            for event in events:
                self.mutate(event)


    def mutate(self, event):
        # method_name