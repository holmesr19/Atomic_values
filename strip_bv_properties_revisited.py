'''Author: Robert Holmes
File name: strip_BV_properties_revisited.py
Description: This will read through a csv row-by-row. It determines what the parcel number on the original
map number is and then slices that off the map number string. If that parcel number is not in the
original parcel numbers string then it is added. The algorithm then makes a record for each element
in the parcel numbers list by prepending the newly constructed map numbers onto a list that contains
the account numbers already. Sometimes, the map numbers derived from the parcel numbers list will be
anomalous due to the way which the parcel numbers list is derived from the "legal1" and "legal3"
fields in the original csv.
Preprocessing: since this algorithm parses a csv, any commas present in the original document should
be replaced with a "}". This is because the python csv package may treat each comma as representing
a new field.'''

import csv
from collections import defaultdict

def main():
    records_read = 0
    records_written = 0
    
    def make_records(map_num, acct_num, parcel_numbers):
        '''takes a list of parcel numbers and concatenates each one onto the end of its proper precursor
        map numbers. it then pairs the newly minted map number with the proper account number and
        writes this entry'''
        write_entry = [acct_num]
        map_num = str(map_num)
        block_num = ''
        counter = 0             #counts the number of dashes in the map_num field. 
        index = 0                #tracks the index position of the current character number
        #print(map_num)
        #print(map_num[index])
        for character in map_num:
            #print(character)
            #character = map_num[index]
            if character == '-':
                counter += 1
                if counter == 4:        #there are 5 levels of classification in the BV map numbering scheme, so it occurs after the 4th dash 
                    print('account number: ', acct_num)
                    print("map number: ", map_num)
                    #print("parcel number: ", map_num[index +1:])
                    block_num = map_num[:index]
                    #print("block number(?): ", block_num)
                    if map_num[index +1:] not in parcel_numbers:
                        parcel_numbers.append(map_num[index +1:])
                    for item in parcel_numbers:    #this might need to be moved to write_records
                        if len(write_entry) == 2:
                            write_entry.pop(0)
                        return_map_num = block_num + '-' + item
                        write_entry.insert(0, return_map_num)
                        write_records(write_entry)
                        #records_written += 1
                    #return_map_num = block_num + str(parcel_numbers) #cant concatenate parcel_numbers list 
                    #print("return map number(?): ", return_map_num)      #to map_num string. or even make it a string.
                    #print("combined parcel number:", write_entry.insert(0, map_num), "\n")  #dumbass.  so you actually can...
                       
            index += 1

    def find_parcel_nums(legal1, legal3):
        '''parses legal1 and legal3 fields to return a list of parcel numbers''' 
        parcel_nums = []
        return_parcel_nums = []
        legal_fields_joined = legal1 + '}' + legal3 + '}'  #joins legal1 and legal3 into one entity with '}'
        i = 0
        current_parcel = ''
        for character in legal_fields_joined:
            if character in ('}', '&'):
                i = 0
                parcel_nums.append(current_parcel)
                current_parcel = ''
            else:
                i += 1
                current_parcel += character
            while '' in parcel_nums:
                parcel_nums.remove('')
        if len(parcel_nums) != 0:
            while '-' in parcel_nums[0]:            
                parcel_nums[0]= parcel_nums[0][1:]
        for element in parcel_nums:
            if ('t' in element or 'T' in element) and not ('p' in element or 'P' in element) and not \
               ('l' in element or 'L' in element) and not ('e' in element or 'E' in element)  and not \
               ('f' in element or 'F' in element) and not ('d' in element or 'D' in element)  and not \
               ('A' in element or 'a' in element) and not ('S' in element or 's' in element):
                #print("element: ", element, "\nlist returned from thru_to_parser: ", thru_to_parser(element))
                parcel_nums.remove(element)
                parcel_nums.extend(thru_to_parser(element))
        return parcel_nums

    def thru_to_parser(consecutive_parcel_nums):
        '''accepts a string that represents consecutive parcel numbers linked with a "thru" or a "to"
        from find_parcel_nums and returns a list starting with the lower boundary and ending with the
        upper boundary'''
        lower_bound = ''
        upper_bound = ''
        thru_to_list = []
        for character in consecutive_parcel_nums:
            try:
                if character not in ('t', 'T') and character != '-':               
                    lower_bound = str(lower_bound) + character
                    print("lower bound: ", lower_bound)
                else:
                    lower_bound = int(lower_bound)
                    break
            except ValueError:
                pass
        for character in reversed(consecutive_parcel_nums):
            try:
                if character not in ('o', 'O', 'u', 'U') and character != '-':
                    upper_bound = character + str(upper_bound)
                else:
                    upper_bound = int(upper_bound)
                    break
            except ValueError:
                pass
        try:
            parcel_range = int(upper_bound) - lower_bound
            i = lower_bound
            while i <= upper_bound:
                thru_to_list.append(str(i))
                i += 1
        except ValueError:
            pass
        #print(thru_to_list)
        return thru_to_list

    def write_records(normalized_record):
        '''open a new csv file to write the new records which it accepts as lists from make_records'''
        with open("/Users/owner/Documents/Winter 2018/BV/RE_out.txt", "a") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(normalized_record)
        
    '''the main code that initiates the normalization process'''
    with open("/Users/owner/Documents/Winter 2018/BV/Live_Input_File_ascii.csv", "r") as csvfile:
        REreader = csv.reader(csvfile)
        for row in REreader:
            #find_parcel_nums(row[2], row[3])
            #records_read += 1
            make_records(row[0], row[1], find_parcel_nums(row[2], row[3]))


if __name__ == '__main__':
    main()
