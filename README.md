# Atomic_values
The purpose of this project is to develop a program that will take two arguments, the first being the key values of the table
and the second being the field with multi-valued attributes. The program uses the Python csv package to read through a csv and
return each row as a list, with each cell in the row being an item in the list. It then picks out the items in each list
corresponding to the key and multi-valued attribute fields designated by the user. The algorithm then creates a new list 
containing only the primary key value at first. It goes on to read through the multi-valued attribute string, slicing the
string at each comma and adding the non-comma strings to a list. The list of non-comma strings is iterated through and matched
each one is added to a list containing the key value until the list of non-comma strings is empty. This set of lists is then 
written to the output file as a csv. 
