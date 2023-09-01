def zeroCountInt(n):
    # Initialize the counter for the number of zeros counted
    count_zeros = 0
    for num in range(1, n+1):
        while(num > 9):    # until all digits are extracted
            digit = num % 10   # get the last digit
            #arr.append(digit)  # add it to the beginning of array
            if digit == 0:
                count_zeros += 1
            num //= 10         # remove last digit
    print("Number of zeros counted in the range", 1, "to", n+1, "is:", count_zeros)
    
    
n =int(input("Enter a number: "))
count = zeroCountInt(n)
print(count)