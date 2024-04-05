import hashlib
from collections import deque

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
    
    def isFull(self):
        return self.left and self.right
    
    def __str__(self):
        return self.data
    
    def isLeaf(self):
        return ((self.left == None) and (self.right == None))

class MerkleTree:
    def __init__(self):
        self.root = None
        self._merkleRoot = ''
        
    def __returnHash(self, x):
        return hashlib.sha256(x.encode()).hexdigest()
        
    def makeTreeFromArray(self, arr):
        def __buildTree(arr, i, n): 
            if i < n: 
                temp = Node(str(arr[i]))  
                temp.left = __buildTree(arr, 2 * i + 1, n)  
                temp.right = __buildTree(arr, 2 * i + 2, n) 
                return temp
            return None
    
        def __addLeafData(arr, node):
            if node is None:
                return
            __addLeafData(arr, node.left)
            if node.isLeaf():
                if arr:
                    node.data = self.__returnHash(arr.pop(0))
                else:
                    node.data = self.__returnHash("")  # Handle case for empty transaction
            else:
                node.data = ''
            __addLeafData(arr, node.right)
    
        nodesReqd = len(arr) * 2 - 1
        self.root = __buildTree([num for num in range(1, nodesReqd + 1)], 0, nodesReqd)
        __addLeafData(arr, self.root)

    def inorderTraversal(self, node):
        if not node:
            return
        
        self.inorderTraversal(node.left)
        print(node)
        self.inorderTraversal(node.right)
    
    def calculateMerkleRoot(self):
        def __merkleHash(node):
            if node.isLeaf():
                return node
            
            left = __merkleHash(node.left).data
            right = __merkleHash(node.right).data
            node.data = self.__returnHash(left + right)
            return node
        
        merkleRoot = __merkleHash(self.root)
        self._merkleRoot = merkleRoot.data
        
        return self._merkleRoot 

    def getMerkleRoot(self):
        return self._merkleRoot    

    def levelOrderTraversal(self, root):
        if not root:
            return
        
        queue = deque()
        queue.append(root)

        level = 0  
        
        while queue:
            level_size = len(queue)
            level_values = []
            
            for _ in range(level_size):
                node = queue.popleft()
                level_values.append(node.data)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            print("Level", level, ":", ", ".join(level_values))
            level += 1 


if __name__ == "__main__":
    transactions = ["Transaction 1", "Transaction 2", "Transaction 3", "Transaction 4", "Transaction 4"]
    while len(transactions) & (len(transactions) - 1) != 0:
        transactions.append("")
    merkle_tree = MerkleTree()
    merkle_tree.makeTreeFromArray(transactions)
    merkle_tree.calculateMerkleRoot()
    print("Merkle Root:", merkle_tree.getMerkleRoot()) 
    merkle_tree.levelOrderTraversal(merkle_tree.root)  


