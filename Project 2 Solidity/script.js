// =============================================================================
//                                  Config 
// =============================================================================

// sets up web3.js
// Web3 calls locally from file web3.min.js
if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} else {
    web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
}

// Default account is the first one
web3.eth.defaultAccount = web3.eth.accounts[0];
// Constant we use later
var GENESIS = '0x0000000000000000000000000000000000000000000000000000000000000000';

// This is the ABI for your contract (get it from Remix, in the 'Compile' tab)
// If you use truffle you can load abi from truffle build folder
// ============================================================
var abi = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "creditor",
				"type": "address"
			},
			{
				"internalType": "uint32",
				"name": "amount",
				"type": "uint32"
			}
		],
		"name": "add_IOU",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint32",
				"name": "amount",
				"type": "uint32"
			}
		],
		"name": "setDebtByUserToUser",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getAllUsers",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "users",
				"type": "address[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			}
		],
		"name": "getDebtByUser",
		"outputs": [
			{
				"internalType": "uint32",
				"name": "ret",
				"type": "uint32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			}
		],
		"name": "getDebtByUserToUser",
		"outputs": [
			{
				"internalType": "uint32",
				"name": "ret",
				"type": "uint32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]; // FIXME: fill this in with your contract's ABI
// ============================================================
abiDecoder.addABI(abi);
// call abiDecoder.decodeMethod to use this - see 'getAllFunctionCalls' for more

// Reads in the ABI
var BlockchainSplitwiseContractSpec = web3.eth.contract(abi);

// This is the address of the contract you want to connect to; copy this from Remix
var contractAddress = '0x6c2109ccD6f207bAA850BFf43d1D06CA00e0311F' // FIXME: fill this in with your contract's address/hash

var BlockchainSplitwise = BlockchainSplitwiseContractSpec.at(contractAddress)


// =============================================================================
//                            Functions To Implement 
// =============================================================================


function getUsers() {
    return BlockchainSplitwise.getAllUsers.call();
}

function getTotalOwed(user) {
    return BlockchainSplitwise.getDebtByUser.call(user).toNumber();
}

function getLastActive(user) {

    var callsArray = getAllFunctionCalls(contractAddress,'setDebtByUserToUser');

    for (let index = 0; index < callsArray.length; index++) {
      if(callsArray[index].args[0]===user.toLowerCase() || callsArray[index].args[1]===user.toLowerCase()){
		var blockNumberOfLatestAct = callsArray[index].blockNo;
		var block = web3.eth.getBlock(blockNumberOfLatestAct, true);
		return block.timestamp;
      }
    }
    return null;
}

function add_IOU(creditor, amount) {
    if(creditor===web3.eth.defaultAccount){
        return
    }
    var prevDebt = BlockchainSplitwise.getDebtByUserToUser.call(web3.eth.defaultAccount,creditor).toNumber();
    amount = +amount + +prevDebt;
    var pathOfUsers = doBFS(creditor,web3.eth.defaultAccount,getNeighbors);
    if(pathOfUsers){
        var minOwePath = Infinity;
        for (let i = 0; i < pathOfUsers.length-1; i++) {
            var debt = BlockchainSplitwise.getDebtByUserToUser.call(pathOfUsers[i],pathOfUsers[i+1]).toNumber();
            minOwePath = Math.min(debt,minOwePath);
        }
        // console.log(minOwePath);   
        if(amount>minOwePath){
            for (let i = 0; i < pathOfUsers.length-1; i++) {
                var debt = BlockchainSplitwise.getDebtByUserToUser.call(pathOfUsers[i],pathOfUsers[i+1]).toNumber();
                BlockchainSplitwise.setDebtByUserToUser.sendTransaction(pathOfUsers[i],pathOfUsers[i+1],debt-minOwePath,{gas : 1000000});  
            }
			BlockchainSplitwise.setDebtByUserToUser.sendTransaction(web3.eth.defaultAccount,creditor,amount-minOwePath,{gas : 1000000});
            return
        }else{
            for (let i = 0; i < pathOfUsers.length-1; i++) {
                var debt = BlockchainSplitwise.getDebtByUserToUser.call(pathOfUsers[i],pathOfUsers[i+1]).toNumber();
                BlockchainSplitwise.setDebtByUserToUser.sendTransaction(pathOfUsers[i],pathOfUsers[i+1],debt-amount,{gas : 1000000});
            }
            return
        }
    }
    BlockchainSplitwise.setDebtByUserToUser.sendTransaction(web3.eth.defaultAccount,creditor,amount,{gas : 1000000});
}

// =============================================================================
//                              Provided Functions 
// =============================================================================
// Reading and understanding these should help you implement the above

// This searches the block history for all calls to 'functionName' (string) on the 'addressOfContract' (string) contract
// It returns an array of objects, one for each call, containing the sender ('from') and arguments ('args')
function getAllFunctionCalls(addressOfContract, functionName) {
    var curBlock = web3.eth.blockNumber;
    var function_calls = [];
    while (curBlock !== GENESIS) {
        var b = web3.eth.getBlock(curBlock, true);
        var txns = b.transactions;
        for (var j = 0; j < txns.length; j++) {
            var txn = txns[j];
            if (txn.to === addressOfContract.toLowerCase()) {
                var func_call = abiDecoder.decodeMethod(txn.input);
                if (func_call && func_call.name === functionName) {
                    var args = func_call.params.map(function(x) { return x.value });
                    function_calls.push({
                        from: txn.from,
                        args: args,
                        blockNo: b.number
                    })
                }
            }
        }
        curBlock = b.parentHash;
    }
    return function_calls;
}

function doBFS(start, end, getNeighbors) {
    var queue = [
        [start]
    ];
    while (queue.length > 0) {
        var cur = queue.shift();
        var lastNode = cur[cur.length - 1]
        if (lastNode === end) {
            return cur;
        } else {
            var neighbors = getNeighbors(lastNode);
            for (var i = 0; i < neighbors.length; i++) {
                queue.push(cur.concat([neighbors[i]]));
            }
        }
    }
    return null;
}

function getNeighbors(node){
    var arrayOfUsers = BlockchainSplitwise.getAllUsers.call();
    var neightbors = []
    for (let i = 0; i < arrayOfUsers.length; i++) {
        var temp = BlockchainSplitwise.getDebtByUserToUser.call(node,arrayOfUsers[i]).toNumber();
        if(temp>0){
            neightbors.push(arrayOfUsers[i])
        }
      }
	return neightbors;
}


// =============================================================================
//                                      UI 
// =============================================================================

// This code updates the 'My Account' UI with the results of your functions
$("#total_owed").html("$" + getTotalOwed(web3.eth.defaultAccount));
$("#last_active").html(timeConverter(getLastActive(web3.eth.defaultAccount)));
$("#myaccount").change(function() {
    web3.eth.defaultAccount = $(this).val();
    $("#total_owed").html("$" + getTotalOwed(web3.eth.defaultAccount));
    $("#last_active").html(timeConverter(getLastActive(web3.eth.defaultAccount)))
});

// Allows switching between accounts in 'My Account' and the 'fast-copy' in 'Address of person you owe
var opts = web3.eth.accounts.map(function(a) { return '<option value="' + a + '">' + a + '</option>' })
$(".account").html(opts);
$(".wallet_addresses").html(web3.eth.accounts.map(function(a) { return '<li>' + a + '</li>' }))

// This code updates the 'Users' list in the UI with the results of your function
$("#all_users").html(getUsers().map(function(u, i) { return "<li>" + u + "</li>" }));

// This runs the 'add_IOU' function when you click the button
// It passes the values from the two inputs above
$("#addiou").click(function() {
    add_IOU($("#creditor").val(), $("#amount").val());
    window.location.reload(true); // refreshes the page after
});

// This is a log function, provided if you want to display things to the page instead of the JavaScript console
// Pass in a discription of what you're printing, and then the object to print
function log(description, obj) {
    $("#log").html($("#log").html() + description + ": " + JSON.stringify(obj, null, 2) + "\n\n");
}