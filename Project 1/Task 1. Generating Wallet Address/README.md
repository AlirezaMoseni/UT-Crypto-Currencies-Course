### **Task1: Generating Valid Bitcoin Addresses**

#### Q1: Test Network Address Generation

`Q1.py` will generate a Bitcoin address for the test network (testnet). The output is in Base58 format, along with the corresponding private key in WIF (Wallet Import Format).

#### Q2: Vanity Address Generation

`Q2.py` will generate a “vanity address.” A vanity address starts with specific characters of your choice. Given three input characters, the code produces an address where those characters appear in positions 2 to 4 (since the first character follows a specific Bitcoin format). The output is again in Base58 format, along with the corresponding private key in WIF.