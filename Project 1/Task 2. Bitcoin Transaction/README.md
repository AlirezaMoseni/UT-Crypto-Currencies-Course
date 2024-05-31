### **Task 2: Bitcoin Transaction Handling with bitcoinlib-python**

In this task, we utilize the `bitcoinlib-python` library to perform Bitcoin transactions on the test network (testnet). The library provides various functions for creating different types of transactions.

#### Q1: Creating a Simple Transaction

In part 1, we create a transaction with one input and two output which The first output cannot be spent by anyone and the second output can be spent by anyone.

In part 2, we spend the spendable output of this transaction in another transaction and return that to our original address as P2PKH output.

#### Q2: Multisig Transaction

in `Q2.py`, 3 addresses are generated first. Next, a transaction with one input and one output of P2MS type is generated which can be spent by 2 of the 3 generated addresses. Finally, using another transaction, this output is spent and the money is returned to the original address.
