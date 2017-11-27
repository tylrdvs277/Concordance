def main():
    files = get_files()
    files_data = get_files_data(files)
    equal_length_files = make_equal(files_data)
    print_diffs(equal_length_files)

def get_files():
    file_num = 1
    files = []
    while file_num <= 2:
        filename = input("Enter file {0}: ".format(file_num))
        try:
            files.append(open(filename, "r"))
            file_num += 1
        except FileNotFoundError:
            print("ERROR: File does not exist")
    return files

def get_files_data(files):
    raw_file_data = []
    for file in files:
        raw_file_data.append([line.strip() for line in file])
    return raw_file_data

def make_equal(files_data):
    min(files_data).extend(["" for _ in range(len(max(files_data)) - len(min(files_data)))])
    return files_data

def print_diffs(files_data):
    for (line_num, (file1, file2)) in enumerate(zip(files_data[0], files_data[1])):
        if file1 != file2:
            print("{0}: {1} | {2}".format(line_num, file1, file2))

if __name__ == "__main__":
    main()
