def extend_string(string_name):
    while(len(string_name) != 7):
        string_name = '0' + string_name
    return(string_name)


def gen_address():
    address_file = open("address.txt", "a")
    for i in range(6864,9999999):
        new_address = 'https://www.imdb.com/title/tt' + extend_string(str(i))
        address_file.write(new_address + '\n')


gen_address()