#############################################################################
# Author: Chelsea Marie Hicks
# OSU Email: hicksche@oregonstate.edu
# Course number/section: CS 325-401
# Assignment: Homework 4            Due Date: April 26, 2020 by 11:59 PM
#
# Description: Program reads a text file named data.txt that contain three
#       values c, k, and n, in which c represents the powers the denomination
#       of coins are (c^0, c^1,...c^k), k represents up to what power those 
#       coins will go to, and n represents the value to make change for.
#       The makeChange algorithm will take the values from the data.txt file
#       and ouput lines containing two values, the denomination of coin and the
#       number of that denomination in the solution, which make up the optimal
#       solution for making change for n cents using the fewest number of coins.
#############################################################################

from collections import OrderedDict 

#utilizes pseudocode from 3b of homework assignment
def makeChange(coins, k, n):
    #create matrix with k+1 rows and n columns initialized to 0
    valMatrix = [[0 for j in range(n+1)] for i in range(k+1)]

    #initialize pennies by setting initial row values to the value of n 
    for j in range(n+1):
        valMatrix[0][j] = j
    
    #nested for loops to go through the least number of coins for every value
    for i in range(1, k+1):
        #if the coin value, c^i, is greater than the amount looked at, bring the previous
        #row value down, otherwise set the value in the matrix to the minimum for that column
        for j in range(1, n+1):
            if coins[i] > j:
                valMatrix[i][j] = valMatrix[i-1][j]
            else:
                valMatrix[i][j] = min(1 + valMatrix[i][j-coins[i]], valMatrix[i-1][j])
    return valMatrix

#function traces matrix to find the optimal solution 
def coinList(valMatrix, coins, k, n):
    coinsUsed = []
    j = n

    #loops from the top down until hitting zero and deducts the coin value used
    #and appends the coin value to the coinsUsed array
    for i in range(k, 0, -1):
        while j >= 0:
            if valMatrix[i][j] < valMatrix[i-1][j]:
                coinsUsed.append(coins[i])
                j -= coins[i]
            else:
                break
        #if the value is less than the second coin, use pennies until hitting zero
        if j < coins[1]:
            while j > 0:
                coinsUsed.append(1)
                j -= 1
    return coinsUsed


def main():
    #open input file with values to read in
    inputFile = open("data.txt", "r")

    #set values from inputFile to their appropriate variables
    for line in inputFile:
        value = [int(variable) for variable in line.split(" ")]
        c = value[0]
        k = value[1]
        n = value[2]
        #create list of coins
        coins = [c**i for i in range(k+1)]

        #fill matrix
        valMatrix = makeChange(coins, k, n)
        #determine the coins used for the optimal solution
        coinsUsed = coinList(valMatrix, coins, k, n)

        #use an ordered dictionary to store the frequency of the coins used
        #start by setting all the key values to the list of coins and equal to 0
        frequency = OrderedDict()
        for val in coins:
            frequency[val] = 0
        #replace the ordered dictionary key values with their frequency from coinsUsed
        for val in coinsUsed:
            if val in frequency:
                frequency[val] += 1
            else:
                frequency[val] = 1

        #write results to file named change.txt
        with open("change.txt", "a") as outputFile:
            for coin,number in frequency.items():
                outputFile.write("Denomination: " + str(coin) + " ")
                outputFile.write("Quantity: " + str(number))
                outputFile.write("\n")
            outputFile.write("\n")
    
    inputFile.close()
    outputFile.close()

main()